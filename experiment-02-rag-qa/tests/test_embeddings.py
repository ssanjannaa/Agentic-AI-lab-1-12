"""
Embedding Dimension Unit Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.embedding_service import LocalDenseEmbedder, calculate_cosine_similarity

def test_local_dense_embedder_dimension():
    embedder = LocalDenseEmbedder(dimension=384)
    vec1 = embedder.embed_text("Firewall and Network Defense")
    vec2 = embedder.embed_text("Stateful inspection firewall filtering")
    
    assert len(vec1) == 384
    assert len(vec2) == 384
    
    sim = calculate_cosine_similarity(vec1, vec2)
    assert 0.0 <= sim <= 1.0
    assert sim > 0.3  # Related topics should have high similarity score
