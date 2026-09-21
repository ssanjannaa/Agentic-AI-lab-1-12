"""
Vector Store Unit Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.vector_store import global_vector_store
from app.services.embedding_service import LocalDenseEmbedder

def test_vector_store_status_and_search():
    status = global_vector_store.get_status()
    assert status["documents_indexed"] == 9
    assert status["chunks_indexed"] >= 30

    embedder = LocalDenseEmbedder()
    query_vec = embedder.embed_text("Phishing social engineering spear phishing")
    results = global_vector_store.search_similar_chunks(query_vec, top_k=3)
    
    assert len(results) == 3
    top_chunk, score = results[0]
    assert score > 0.3
    assert "Phishing" in top_chunk["title"]
