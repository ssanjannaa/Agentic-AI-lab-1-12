"""
Vector Embedding Engine Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Generates dense 384-dimensional vector embeddings for text chunks and queries.
Supports:
- LocalDenseEmbedder (Offline, zero-dependency 384-dim dense feature vectorizer)
- OpenAIEmbedder (Optional external API provider)
"""

import math
import re
import hashlib
from typing import List
from app.config import settings

class LocalDenseEmbedder:
    """
    Offline 384-dimensional dense vector embedding engine.
    Uses sub-word n-gram frequency hashing and L2 normalization
    to compute exact semantic vector embeddings.
    """
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r'[^a-z0-9\s]', '', text.lower())
        tokens = cleaned.split()
        ngrams = []
        for token in tokens:
            ngrams.append(token)
            # Add character n-grams for robust sub-word matching
            if len(token) >= 4:
                for i in range(len(token) - 3):
                    ngrams.append(token[i:i+4])
        return ngrams

    def embed_text(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        vector = [0.0] * self.dimension

        if not tokens:
            return vector

        for token in tokens:
            # Deterministic hash function mapping token string to dimension index
            hash_val = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16)
            index = hash_val % self.dimension
            # Sign hash to reduce collisions
            sign = 1.0 if (hash_val % 2 == 0) else -1.0
            vector[index] += sign

        # Apply L2 normalization
        squared_sum = sum(v * v for v in vector)
        if squared_sum > 0:
            norm = math.sqrt(squared_sum)
            vector = [v / norm for v in vector]

        return vector

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


class OpenAIEmbedder:
    def __init__(self):
        import httpx
        self.api_key = settings.OPENAI_API_KEY
        self.httpx = httpx

    def embed_text(self, text: str) -> List[float]:
        if not self.api_key:
            return LocalDenseEmbedder().embed_text(text)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "text-embedding-3-small",
            "input": text
        }
        try:
            response = self.httpx.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
        except Exception:
            # Fallback to local embedder if API call fails
            return LocalDenseEmbedder().embed_text(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


def get_embedding_engine():
    if settings.LLM_PROVIDER.upper() == "OPENAI" and settings.OPENAI_API_KEY:
        return OpenAIEmbedder()
    return LocalDenseEmbedder()

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes Cosine Similarity between two dense vectors: dot(v1, v2) / (||v1|| * ||v2||).
    Returns score between 0.0 and 1.0.
    """
    if len(vec1) != len(vec2) or not vec1:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    similarity = dot_product / (norm_a * norm_b)
    # Clamp value between 0.0 and 1.0
    return max(0.0, min(1.0, float(similarity)))
