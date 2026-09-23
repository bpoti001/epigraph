import numpy as np
from sklearn.cluster import DBSCAN
from typing import Dict, List, Tuple, Any, Optional

class IncrementalDeduplicator:
    """Incremental K-NN and DBSCAN deduplicator replacing the O(n^2) pairwise matrix."""

    def __init__(self, similarity_threshold: float = 0.88):
        self.similarity_threshold = similarity_threshold
        # In cosine distance: dist = 1 - sim
        self.eps = 1.0 - similarity_threshold

    def find_clusters(self, entity_ids: List[str], embeddings: np.ndarray) -> List[List[str]]:
        """Cluster candidate entities using DBSCAN in O(n log n) with spatial index."""
        if len(entity_ids) < 2:
            return []

        # DBSCAN with cosine metric
        clustering = DBSCAN(eps=self.eps, min_samples=2, metric="cosine")
        labels = clustering.fit_predict(embeddings)

        clusters = {}
        for idx, label in enumerate(labels):
            if label != -1:  # -1 is noise (no duplicate)
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(entity_ids[idx])

        return list(clusters.values())

    def resolve_cluster_winner(self, cluster_entity_ids: List[str], metadata: Dict[str, Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Deterministic tie-breaker:
        1. Higher access count
        2. Higher PageRank score
        3. Lexicographical ID
        Returns (winner_id, [loser_ids])
        """
        def sort_key(eid):
            meta = metadata.get(eid, {})
            access = meta.get("access_count", 0)
            pr = meta.get("pagerank", 0.0)
            return (-access, -pr, eid)

        sorted_candidates = sorted(cluster_entity_ids, key=sort_key)
        winner = sorted_candidates[0]
        losers = sorted_candidates[1:]
        return winner, losers
