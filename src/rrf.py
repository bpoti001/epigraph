import re
from typing import Dict, List, Tuple, Set

class DynamicIntentRRF:
    def __init__(self, k: int = 60):
        self.k = k
        self.temporal_keywords = {"when", "date", "year", "time", "month", "day", "after", "before", "yesterday", "ago", "last"}
        self.relational_keywords = {"why", "how", "connect", "both", "relationship", "because", "between", "cause", "transition", "pursue", "likely"}

    def classify_intent_weights(self, query: str) -> Dict[str, float]:
        tokens = set(re.findall(r"\w+", query.lower()))

        is_temporal = bool(tokens & self.temporal_keywords)
        is_relational = bool(tokens & self.relational_keywords)

        if is_temporal and is_relational:
            return {"vector": 0.30, "graph": 0.40, "bm25": 0.40}
        elif is_temporal:
            return {"vector": 0.30, "graph": 0.35, "bm25": 0.45}
        elif is_relational:
            return {"vector": 0.30, "graph": 0.45, "bm25": 0.35}
        else:
            # Default balanced hybrid
            return {"vector": 0.35, "graph": 0.35, "bm25": 0.35}

    def fuse(self, ranked_legs: Dict[str, List[str]], weights: Dict[str, float]) -> List[Tuple[str, float]]:
        all_candidates: Set[str] = set()
        for cand_list in ranked_legs.values():
            all_candidates.update(cand_list)

        rrf_scores: Dict[str, float] = {cand: 0.0 for cand in all_candidates}

        for leg_name, cand_list in ranked_legs.items():
            w = weights.get(leg_name, 1.0)
            for rank_0, cand_id in enumerate(cand_list):
                rank_1 = rank_0 + 1
                rrf_scores[cand_id] += w / (self.k + rank_1)

        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
