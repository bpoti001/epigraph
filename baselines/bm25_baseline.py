from typing import Dict, List, Tuple, Any
from src.bm25 import BM25Index

class BM25Baseline:
    def __init__(self):
        self.bm25 = BM25Index()

    def ingest(self, conversation_dict: Dict[str, Any]):
        doc_ids = []
        doc_texts = []

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
                doc_ids.append(dia_id)
                doc_texts.append(enriched_text)

        self.bm25.build_index(doc_ids, doc_texts)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        return self.bm25.score(query, top_k=top_k)
