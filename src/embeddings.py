import os
import torch
import numpy as np
from typing import List, Union
from transformers import AutoTokenizer, AutoModel

class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        self.cache = {}

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embed_texts(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        all_embeddings = []
        uncached_indices = []
        uncached_texts = []

        for idx, text in enumerate(texts):
            if text in self.cache:
                all_embeddings.append(self.cache[text])
            else:
                all_embeddings.append(None)
                uncached_indices.append(idx)
                uncached_texts.append(text)

        if uncached_texts:
            for i in range(0, len(uncached_texts), batch_size):
                batch = uncached_texts[i:i + batch_size]
                encoded = self.tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt").to(self.device)
                with torch.no_grad():
                    output = self.model(**encoded)
                    embeddings = self._mean_pooling(output, encoded["attention_mask"])
                    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                    batch_vecs = embeddings.cpu().numpy()

                for j, text in enumerate(batch):
                    vec = batch_vecs[j]
                    self.cache[text] = vec
                    orig_idx = uncached_indices[i + j]
                    all_embeddings[orig_idx] = vec

        return np.array(all_embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed_texts([query])[0]
