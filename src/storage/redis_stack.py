import json
import logging
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

try:
    import redis
    from redis.commands.search.field import TextField, VectorField, TagField, NumericField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

logger = logging.getLogger("epigraph.redis")

class RedisStackStore:
    """Redis Stack client supporting RedisJSON documents, HNSW vector search, and BM25 text search."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, index_name: str = "idx:epigraph_ltm", dim: int = 384):
        self.host = host
        self.port = port
        self.db = db
        self.index_name = index_name
        self.dim = dim
        self.client: Optional[Any] = None
        self.is_connected = False
        self._in_memory_docs: Dict[str, Dict[str, Any]] = {}
        self._in_memory_vectors: Dict[str, np.ndarray] = {}

        if HAS_REDIS:
            try:
                self.client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=False)
                self.client.ping()
                self.is_connected = True
                self._init_index()
                logger.info(f"Connected to Redis Stack at {host}:{port}")
            except Exception as e:
                logger.warning(f"Redis Stack not reachable at {host}:{port} ({e}). Operating in memory-fallback mode.")
                self.is_connected = False
        else:
            self.is_connected = False

    def _init_index(self):
        if not self.is_connected or not self.client:
            return

        try:
            self.client.ft(self.index_name).info()
        except Exception:
            schema = (
                TextField("$.text", as_name="text", weight=2.0),
                TextField("$.speaker", as_name="speaker", weight=1.5),
                TagField("$.session_id", as_name="session_id"),
                NumericField("$.access_count", as_name="access_count"),
                NumericField("$.confidence", as_name="confidence"),
                VectorField(
                    "$.embedding",
                    "HNSW",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.dim,
                        "DISTANCE_METRIC": "COSINE",
                        "M": 16,
                        "EF_CONSTRUCTION": 200,
                        "EF_RUNTIME": 50,
                    },
                    as_name="vector"
                )
            )
            definition = IndexDefinition(prefix=["doc:"], index_type=IndexType.JSON)
            self.client.ft(self.index_name).create_index(schema, definition=definition)
            logger.info(f"Created RediSearch HNSW index '{self.index_name}' with dim={self.dim}")

    def upsert_fact(self, fact_id: str, text: str, embedding: np.ndarray, metadata: Optional[Dict[str, Any]] = None, deduplicate: bool = True) -> Tuple[str, bool]:
        """Insert or update fact. If similarity > 0.95, bumps access count instead of duplicating."""
        meta = metadata or {}
        vec_bytes = embedding.astype(np.float32).tobytes()

        # L0 Ingestion Deduplication check
        if deduplicate:
            dup_id = self.check_near_duplicate(embedding, threshold=0.95)
            if dup_id:
                self.bump_access_count(dup_id)
                return dup_id, False  # Existing duplicate merged

        doc = {
            "id": fact_id,
            "text": text,
            "speaker": meta.get("speaker", ""),
            "session_id": meta.get("session_id", ""),
            "access_count": meta.get("access_count", 1),
            "confidence": meta.get("confidence", 1.0),
            "embedding": embedding.tolist()
        }

        if self.is_connected and self.client:
            key = f"doc:{fact_id}"
            pipe = self.client.pipeline(transaction=True)
            pipe.json().set(key, "$", doc)
            # Add to DedupRegistry sorted set (keyed by timestamp or access) atomically
            pipe.zadd("registry:dedup_queue", {fact_id: meta.get("timestamp_epoch", 0.0)})
            pipe.execute()
        else:
            self._in_memory_docs[fact_id] = doc
            self._in_memory_vectors[fact_id] = embedding

        return fact_id, True

    def check_near_duplicate(self, embedding: np.ndarray, threshold: float = 0.95) -> Optional[str]:
        """Check if an existing vector has cosine similarity > threshold (distance < 1 - threshold)."""
        if self.is_connected and self.client:
            max_dist = 1.0 - threshold
            q = Query(f"*=>[KNN 1 @vector $query_vec AS dist]").return_fields("id", "dist").paging(0, 1).dialect(2)
            res = self.client.ft(self.index_name).search(q, query_params={"query_vec": embedding.astype(np.float32).tobytes()})
            if res.docs:
                closest_doc = res.docs[0]
                dist = float(getattr(closest_doc, "dist", 1.0))
                if dist <= max_dist:
                    return closest_doc.id.replace("doc:", "")
        else:
            for fid, vec in self._in_memory_vectors.items():
                sim = float(np.dot(embedding, vec) / (np.linalg.norm(embedding) * np.linalg.norm(vec) + 1e-9))
                if sim >= threshold:
                    return fid
        return None

    def bump_access_count(self, fact_id: str):
        if self.is_connected and self.client:
            key = f"doc:{fact_id}"
            try:
                self.client.json().numincrby(key, "$.access_count", 1)
            except Exception:
                pass
        elif fact_id in self._in_memory_docs:
            self._in_memory_docs[fact_id]["access_count"] += 1

    def vector_search(self, query_vec: np.ndarray, top_k: int = 20) -> List[Tuple[str, float]]:
        """HNSW Approximate Nearest Neighbor vector search."""
        if self.is_connected and self.client:
            q = Query(f"*=>[KNN {top_k} @vector $query_vec AS dist]").return_fields("id", "dist").sort_by("dist").paging(0, top_k).dialect(2)
            res = self.client.ft(self.index_name).search(q, query_params={"query_vec": query_vec.astype(np.float32).tobytes()})
            results = []
            for doc in res.docs:
                fid = doc.id.replace("doc:", "")
                dist = float(getattr(doc, "dist", 1.0))
                sim = 1.0 - dist
                results.append((fid, sim))
            return results
        else:
            sims = []
            for fid, vec in self._in_memory_vectors.items():
                s = float(np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec) + 1e-9))
                sims.append((fid, s))
            sims.sort(key=lambda x: x[1], reverse=True)
            return sims[:top_k]

    def bm25_search(self, query_str: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """Okapi BM25 keyword search over text fields."""
        if self.is_connected and self.client:
            q = Query(query_str).paging(0, top_k).with_scores()
            res = self.client.ft(self.index_name).search(q)
            results = []
            for doc in res.docs:
                fid = doc.id.replace("doc:", "")
                score = float(getattr(doc, "score", 1.0))
                results.append((fid, score))
            return results
        else:
            # Simple in-memory fallback
            words = set(query_str.lower().split())
            scores = []
            for fid, doc in self._in_memory_docs.items():
                doc_words = set(doc["text"].lower().split())
                overlap = len(words & doc_words)
                if overlap > 0:
                    scores.append((fid, float(overlap)))
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:top_k]
