import numpy as np
from typing import Dict, List, Tuple, Any
from src.embeddings import EmbeddingEngine

class DenseVectorRAG:
    def __init__(self, embedding_engine: EmbeddingEngine):
        self.embedder = embedding_engine
        self.turn_ids: List[str] = []
        self.turn_texts: List[str] = []
        self.turn_embeddings: np.ndarray = None

    def ingest(self, conversation_dict: Dict[str, Any]):
        self.turn_ids = []
        self.turn_texts = []

        session_keys = [k for k in conversation_dict.keys() if k.startswith("session_") and not k.endswith("_date_time")]
        session_keys = sorted(session_keys, key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 999)

        for sk in session_keys:
            dt = conversation_dict.get(sk + "_date_time", "")
            turns = conversation_dict.get(sk, [])
            for turn in turns:
                dia_id = turn.get("dia_id")
                speaker = turn.get("speaker", "")
                text = turn.get("text", "")
                enriched_text = f"[{speaker}] (Session {sk}, {dt}): {text}"
                self.turn_ids.append(dia_id)
                self.turn_texts.append(enriched_text)

        self.turn_embeddings = self.embedder.embed_texts(self.turn_texts, batch_size=128)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        if not self.turn_ids:
            return []
        q_vec = self.embedder.embed_query(query)
        sims = np.dot(self.turn_embeddings, q_vec)
        top_indices = np.argsort(-sims)[:top_k]
        return [(self.turn_ids[i], float(sims[i])) for i in top_indices]
