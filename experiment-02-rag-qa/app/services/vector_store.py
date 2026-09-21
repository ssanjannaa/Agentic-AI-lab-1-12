"""
Vector Store Index Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Indexes document chunks into a vector store, computes cosine similarity,
and persists index metadata to index/vector_index.json.
"""

import os
import json
import datetime
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.services.document_loader import load_knowledge_base_documents
from app.services.chunking_service import chunk_all_documents, Chunk
from app.services.embedding_service import get_embedding_engine, calculate_cosine_similarity

class VectorStore:
    def __init__(self, index_path: str = None):
        if index_path is None:
            index_path = settings.INDEX_PATH
        self.index_path = index_path
        self.embedding_engine = get_embedding_engine()
        self.index_data = {
            "last_indexed": "",
            "document_count": 0,
            "chunk_count": 0,
            "embedding_model": settings.EMBEDDING_MODEL,
            "vector_store": "LocalJSONVectorStore",
            "entries": []
        }
        self.load_index()

    def build_index(self) -> Dict[str, Any]:
        """
        Loads all documents from knowledge_base/, chunks them,
        generates vector embeddings, and saves the index to disk.
        """
        documents = load_knowledge_base_documents()
        chunks = chunk_all_documents(documents)

        entries = []
        for chunk in chunks:
            vector = self.embedding_engine.embed_text(chunk.text)
            entries.append({
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "source": chunk.source,
                "title": chunk.title,
                "start_char": chunk.start_char,
                "end_char": chunk.end_char,
                "text": chunk.text,
                "vector": vector
            })

        self.index_data = {
            "last_indexed": datetime.datetime.now().isoformat(),
            "document_count": len(documents),
            "chunk_count": len(entries),
            "embedding_model": settings.EMBEDDING_MODEL,
            "vector_store": "LocalJSONVectorStore",
            "entries": entries
        }

        self.save_index()
        return self.get_status()

    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index_data, f, indent=2)

    def load_index(self) -> bool:
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    self.index_data = json.load(f)
                return True
            except Exception:
                pass
        return False

    def search_similar_chunks(self, query_vector: List[float], top_k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        """
        Calculates Cosine Similarity between query_vector and all indexed chunk vectors.
        Returns top-K sorted list of (chunk_dict, similarity_score).
        """
        if not self.index_data.get("entries"):
            # Auto-build index if missing
            self.build_index()

        results = []
        for entry in self.index_data.get("entries", []):
            chunk_vector = entry["vector"]
            score = calculate_cosine_similarity(query_vector, chunk_vector)
            results.append((entry, score))

        # Sort by similarity score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "ready" if self.index_data.get("entries") else "empty",
            "documents_indexed": self.index_data.get("document_count", 0),
            "chunks_indexed": self.index_data.get("chunk_count", 0),
            "embedding_model": self.index_data.get("embedding_model", settings.EMBEDDING_MODEL),
            "vector_store": self.index_data.get("vector_store", "LocalJSONVectorStore"),
            "last_indexed": self.index_data.get("last_indexed", "Never")
        }

global_vector_store = VectorStore()

if __name__ == "__main__":
    status = global_vector_store.build_index()
    print(f"[OK] Built vector index: {status}")
