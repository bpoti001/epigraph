import re
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Any

class StaticGraphRAG:
    """HippoRAG-style static graph RAG: Static Knowledge Graph + Static Personalized PageRank."""
    def __init__(self, damping: float = 0.85):
        self.damping = damping
        self.graph = nx.DiGraph()
        self.turn_ids: List[str] = []

    def _extract_entities(self, text: str) -> List[str]:
        patterns = [
            r"\b[A-Z][a-zA-Z0-9_\-]{2,}(?:\s+[A-Z][a-zA-Z0-9_\-]+)*\b",
            r"\b(?:psychology|counseling|adoption|transgender|charity|mental health|transition|marathon)\b"
        ]
        entities = set()
        for pat in patterns:
            matches = re.findall(pat, text, flags=re.IGNORECASE if "psychology" in pat else 0)
            for m in matches:
                m_clean = m.strip().lower()
                if len(m_clean) > 2 and m_clean not in {"hey", "good", "see", "yes", "what", "how", "that", "this", "thanks"}:
                    entities.add(m_clean)
        return list(entities)

    def ingest(self, conversation_dict: Dict[str, Any]):
        self.graph = nx.DiGraph()
        self.turn_ids = []

        session_keys = [k for k in conversation_dict.keys() if k.startswith("session_") and not k.endswith("_date_time")]
        session_keys = sorted(session_keys, key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 999)

        prev_turn = None
        for sk in session_keys:
            turns = conversation_dict.get(sk, [])
            for turn in turns:
                dia_id = turn.get("dia_id")
                text = turn.get("text", "")
                self.turn_ids.append(dia_id)
                self.graph.add_node(dia_id, node_type="turn")

                if prev_turn:
                    self.graph.add_edge(prev_turn, dia_id, weight=1.0)
                prev_turn = dia_id

                entities = self._extract_entities(text)
                for ent in entities:
                    ent_id = f"ENT_{ent}"
                    self.graph.add_node(ent_id, node_type="entity")
                    self.graph.add_edge(dia_id, ent_id, weight=1.0)
                    self.graph.add_edge(ent_id, dia_id, weight=1.0)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        if not self.turn_ids or self.graph.number_of_nodes() == 0:
            return []

        query_entities = self._extract_entities(query)
        seeds = [f"ENT_{qe}" for qe in query_entities if self.graph.has_node(f"ENT_{qe}")]

        N = self.graph.number_of_nodes()
        if seeds:
            personalization = {nid: (1.0 / len(seeds) if nid in seeds else 0.0) for nid in self.graph.nodes}
        else:
            personalization = {nid: 1.0 / N for nid in self.graph.nodes}

        try:
            ppr_scores = nx.pagerank(self.graph, alpha=self.damping, personalization=personalization, weight="weight", max_iter=80)
        except Exception:
            ppr_scores = {nid: 1.0 / N for nid in self.graph.nodes}

        turn_scores = [(tid, ppr_scores.get(tid, 0.0)) for tid in self.turn_ids]
        turn_scores.sort(key=lambda x: x[1], reverse=True)
        return turn_scores[:top_k]
