import math
import re
from collections import Counter
from typing import List, Dict, Tuple

class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_ids: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = {}  # term -> {doc_idx: freq}
        self.num_docs: int = 0

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        return [w for w in cleaned.split() if len(w) > 1]

    def build_index(self, doc_ids: List[str], documents: List[str]):
        self.doc_ids = doc_ids
        self.num_docs = len(documents)
        self.doc_lengths = []
        self.doc_freqs = {}
        self.inverted_index = {}

        total_length = 0
        for idx, doc in enumerate(documents):
            tokens = self._tokenize(doc)
            length = len(tokens)
            self.doc_lengths.append(length)
            total_length += length

            counts = Counter(tokens)
            for term, freq in counts.items():
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                    self.doc_freqs[term] = 0
                self.inverted_index[term][idx] = freq
                self.doc_freqs[term] += 1

        self.avg_doc_len = total_length / max(1, self.num_docs)

    def score(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        query_terms = self._tokenize(query)
        if not query_terms or self.num_docs == 0:
            return []

        doc_scores: Dict[int, float] = {}

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            df = self.doc_freqs[term]
            # Standard Lucene/BM25 IDF formula
            idf = math.log(1.0 + (self.num_docs - df + 0.5) / (df + 0.5))

            for doc_idx, tf in self.inverted_index[term].items():
                doc_len = self.doc_lengths[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                term_score = idf * (numerator / denominator)

                doc_scores[doc_idx] = doc_scores.get(doc_idx, 0.0) + term_score

        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.doc_ids[idx], score) for idx, score in sorted_docs]
