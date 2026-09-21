"""
Out-of-Knowledge-Base Query Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.rag_service import process_rag_query

def test_out_of_kb_retrieval_threshold():
    res = retrieve_relevant_chunks("What is the capital of France?", top_k=4)
    assert res["is_out_of_scope"] is True
    assert res["max_score"] < 0.25

def test_out_of_kb_rag_answer():
    res = process_rag_query("What is the capital of France?", top_k=4)
    assert res["success"] is True
    assert len(res["sources"]) == 0
    assert "does not contain sufficient information" in res["answer"].lower()
