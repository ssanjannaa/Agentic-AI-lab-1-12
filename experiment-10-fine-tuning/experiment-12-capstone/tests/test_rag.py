"""
RAG Engine & Indexing Unit Tests
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

from app.services.rag_engine import rag_engine

def test_rag_index_loaded():
    assert rag_engine.index_loaded is True
    stats = rag_engine.get_stats()
    assert stats["total_documents"] >= 5
    assert stats["total_indexed_chunks"] >= 5

def test_rag_retrieval_phishing_query():
    results = rag_engine.retrieve("phishing email spearphishing link lure", top_k=3)
    assert len(results) > 0
    assert any("phishing" in item.document_name.lower() or "kb_02" in item.document_name.lower() for item in results)
    assert results[0].relevance_score > 0.0

def test_rag_retrieval_sqli_query():
    results = rag_engine.retrieve("sql injection union select web attack", top_k=3)
    assert len(results) > 0
    assert any("sqli" in item.document_name.lower() or "kb_03" in item.document_name.lower() for item in results)

def test_rag_retrieval_empty_query():
    results = rag_engine.retrieve("", top_k=3)
    assert len(results) == 0
