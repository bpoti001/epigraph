import re
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Set
from src.embeddings import EmbeddingEngine
from src.bm25 import BM25Index
from src.graph_memory import DynamicCognitiveGraph
from src.rrf import DynamicIntentRRF

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "about",
    "against", "between", "into", "through", "during", "before", "after", "above", "below",
    "from", "up", "down", "of", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "can", "will", "just", "don", "should", "now", "hey",
    "good", "see", "yes", "what", "that", "this", "thanks", "well", "like", "really",
    "much", "know", "think", "sure", "great", "sound", "sounds", "feel", "feels", "going"
}

class EpiGraphPipeline:
    def __init__(self, embedding_engine: EmbeddingEngine):
        self.embedder = embedding_engine
        self.bm25 = BM25Index()
        self.graph = DynamicCognitiveGraph(damping=0.85)
        self.rrf = DynamicIntentRRF(k=60)
        self.turn_ids: List[str] = []
        self.turn_texts: List[str] = []
        self.turn_embeddings: Optional[np.ndarray] = None
        self.turn_meta: Dict[str, Dict[str, Any]] = {}

    def _extract_entities(self, text: str) -> List[str]:
        """Extract high-signal entities, proper nouns, and domain keywords."""
        entities: Set[str] = set()

        # 1. Capitalized words/phrases (e.g. Caroline, Melanie, LGBTQ, Dr. Seuss)
        capitalized = re.findall(r"\b[A-Z][a-zA-Z0-9_\-\']*(?:\s+[A-Z][a-zA-Z0-9_\-\']*)*\b", text)
        for cap in capitalized:
            c_clean = cap.strip().lower()
            if len(c_clean) > 2 and c_clean not in STOPWORDS:
                entities.add(c_clean)

        # 2. Significant content words (nouns/adjectives)
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        for w in words:
            if w not in STOPWORDS and len(w) > 3:
                entities.add(w)

        return list(entities)

    def ingest_locomo_conversation(self, conversation_dict: Dict[str, Any]):
        """Ingest multi-session conversation into the dual-store and graph."""
        self.graph = DynamicCognitiveGraph(damping=0.85)
        self.turn_ids = []
        self.turn_texts = []
        self.turn_meta = {}

        session_keys = [k for k in conversation_dict.keys() if k.startswith("session_") and not k.endswith("_date_time")]
        session_keys = sorted(session_keys, key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 999)

        all_doc_ids = []
        all_doc_texts = []

        prev_session_node = None

        for sk in session_keys:
            dt_key = sk + "_date_time"
            dt = conversation_dict.get(dt_key, "")
            turns = conversation_dict.get(sk, [])
            if not turns:
                continue

            session_node_id = f"SESSION_{sk}"
            self.graph.add_node(session_node_id, label=f"Session {sk} ({dt})", node_type="session_anchor", timestamp=dt)

            if prev_session_node:
                self.graph.add_edge(prev_session_node, session_node_id, rel_type="SESSION_PRECEDES", weight=1.5)
            prev_session_node = session_node_id

            prev_turn_id = None
            for turn in turns:
                dia_id = turn.get("dia_id")
                speaker = turn.get("speaker", "")
                text = turn.get("text", "")
                enriched_text = f"[{speaker}] (Session {sk}, {dt}): {text}"

                self.turn_ids.append(dia_id)
                self.turn_texts.append(enriched_text)
                self.turn_meta[dia_id] = {
                    "dia_id": dia_id,
                    "speaker": speaker,
                    "text": text,
                    "session": sk,
                    "datetime": dt
                }

                all_doc_ids.append(dia_id)
                all_doc_texts.append(enriched_text)

                # Add turn node to graph
                self.graph.add_node(dia_id, label=enriched_text, node_type="turn", session_id=sk, timestamp=dt)
                self.graph.add_edge(session_node_id, dia_id, rel_type="CONTAINS_TURN", weight=1.0)

                # Sequential edge between turns in the same session
                if prev_turn_id:
                    self.graph.add_edge(prev_turn_id, dia_id, rel_type="TEMPORAL_NEXT", weight=1.5)
                    self.graph.add_edge(dia_id, prev_turn_id, rel_type="TEMPORAL_PREV", weight=1.0)
                prev_turn_id = dia_id

                # Speaker node
                if speaker:
                    spk_id = f"SPK_{speaker.lower()}"
                    self.graph.add_node(spk_id, label=speaker, node_type="speaker")
                    self.graph.add_edge(dia_id, spk_id, rel_type="SPOKEN_BY", weight=1.8)
                    self.graph.add_edge(spk_id, dia_id, rel_type="UTTERED", weight=1.0)

                # Extract entities and connect them bidirectional
                entities = self._extract_entities(text)
                for ent in entities:
                    ent_node_id = f"ENT_{ent}"
                    self.graph.add_node(ent_node_id, label=ent, node_type="entity")
                    self.graph.add_edge(dia_id, ent_node_id, rel_type="MENTIONS", weight=2.0)
                    self.graph.add_edge(ent_node_id, dia_id, rel_type="APPEARS_IN", weight=1.5)

        # 1. Build Dense Vector Index
        self.turn_embeddings = self.embedder.embed_texts(all_doc_texts, batch_size=128)
        for idx, dia_id in enumerate(self.turn_ids):
            self.graph.nodes[dia_id].embedding = self.turn_embeddings[idx]

        # 2. Build BM25 Keyword Index
        self.bm25.build_index(all_doc_ids, all_doc_texts)

        # 3. Run Initial Dreaming Consolidation
        self.run_consolidation()

    def run_consolidation(self):
        """Execute the Dreaming State consolidation."""
        self.graph.partition_communities()
        self.graph.identify_god_nodes(std_mult=1.0)
        self.graph.apply_catd(grace_cycles=4)

    def retrieve(self, query: str, top_k: int = 10, record_usage: bool = True) -> List[Tuple[str, float]]:
        """Multi-leg retrieval fusing Dense Vector, U-PPR Graph Traversal, Multi-Hop Expansion, and BM25."""
        if not self.turn_ids:
            return []

        # --- Leg 1: Dense Semantic Vector Search ---
        q_vec = self.embedder.embed_query(query)
        cos_sims = np.dot(self.turn_embeddings, q_vec)
        top_vec_indices = np.argsort(-cos_sims)[:30]
        leg1_vector_turns = [self.turn_ids[i] for i in top_vec_indices]

        # --- Leg 3: Okapi BM25 Keyword Search ---
        bm25_res = self.bm25.score(query, top_k=30)
        leg3_bm25_turns = [doc_id for doc_id, _ in bm25_res]

        # --- Leg 2: Graph U-PPR Traversal with Multi-Hop Spreading ---
        query_entities = self._extract_entities(query)
        seed_nodes = []
        seed_weights = []

        # High priority seeds from query entities
        for qe in query_entities:
            ent_id = f"ENT_{qe}"
            if ent_id in self.graph.nodes:
                seed_nodes.append(ent_id)
                seed_weights.append(3.0)
            spk_id = f"SPK_{qe}"
            if spk_id in self.graph.nodes:
                seed_nodes.append(spk_id)
                seed_weights.append(4.0)

        # Top BM25 and Vector hits serve as episodic entry points
        for dia_id in leg3_bm25_turns[:3]:
            if dia_id in self.graph.nodes:
                seed_nodes.append(dia_id)
                seed_weights.append(2.0)

        for dia_id in leg1_vector_turns[:3]:
            if dia_id in self.graph.nodes:
                seed_nodes.append(dia_id)
                seed_weights.append(1.5)

        uppr_scores = self.graph.compute_uppr(seed_nodes, seed_weights)

        # Multi-Hop Neighborhood Expansion:
        # Boost turns directly reachable within 2 hops of top seed turns across sessions
        multi_hop_scores: Dict[str, float] = {}
        for nid in self.turn_ids:
            if nid in uppr_scores:
                multi_hop_scores[nid] = uppr_scores[nid]

        # Traverse neighbors of top seeds
        for seed_id in seed_nodes[:8]:
            if self.graph.graph.has_node(seed_id):
                for neighbor in self.graph.graph.neighbors(seed_id):
                    if neighbor in multi_hop_scores:
                        multi_hop_scores[neighbor] += 0.08
                    # 2nd hop
                    for hop2 in self.graph.graph.neighbors(neighbor):
                        if hop2 in multi_hop_scores:
                            multi_hop_scores[hop2] += 0.04

        turn_uppr = [(nid, multi_hop_scores.get(nid, 0.0)) for nid in self.turn_ids]
        turn_uppr.sort(key=lambda x: x[1], reverse=True)
        leg2_graph_turns = [nid for nid, _ in turn_uppr[:30]]

        # --- Dynamic Intent Weighting & Reciprocal Rank Fusion ---
        weights = self.rrf.classify_intent_weights(query)
        ranked_legs = {
            "vector": leg1_vector_turns,
            "graph": leg2_graph_turns,
            "bm25": leg3_bm25_turns
        }

        fused = self.rrf.fuse(ranked_legs, weights)
        final_top = fused[:top_k]

        # --- Usage Plasticity Feedback ---
        if record_usage and final_top:
            top_retrieved_ids = [cand_id for cand_id, _ in final_top[:3]]
            self.graph.record_usage(top_retrieved_ids)

        return final_top
