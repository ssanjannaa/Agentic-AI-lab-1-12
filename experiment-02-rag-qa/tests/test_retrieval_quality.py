"""
Deterministic Retrieval Quality & Regression Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.rag_service import process_rag_query

def test_sql_injection_retrieval_regression():
    res = retrieve_relevant_chunks("What is SQL injection?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    assert res["max_score"] >= 0.25
    top_doc = sources[0]["document"]
    assert "Web Application Security" in top_doc
    
    rag_res = process_rag_query("What is SQL injection?")
    assert rag_res["success"]
    assert len(rag_res["sources"]) > 0
    assert not rag_res["inspector"]["out_of_scope"]

def test_sqli_acronym_retrieval_regression():
    res = retrieve_relevant_chunks("What is SQLi?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Web Application Security" in top_doc

def test_retrieval_phishing_quality():
    res = retrieve_relevant_chunks("What is phishing?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Phishing" in top_doc

def test_retrieval_ransomware_quality():
    res = retrieve_relevant_chunks("What is ransomware?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Ransomware" in top_doc or "Malware" in top_doc

def test_retrieval_firewall_quality():
    res = retrieve_relevant_chunks("What does a firewall do?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Firewall" in top_doc or "Network Defense" in top_doc

def test_mfa_acronym_retrieval_regression():
    res = retrieve_relevant_chunks("Explain MFA", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Authentication" in top_doc or "Access Control" in top_doc

def test_incident_response_retrieval_regression():
    res = retrieve_relevant_chunks("What are the phases of incident response?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Incident Response" in top_doc

def test_security_monitoring_retrieval_regression():
    res = retrieve_relevant_chunks("What is security monitoring?", top_k=4)
    sources = res["sources"]
    assert len(sources) > 0
    assert not res["is_out_of_scope"]
    top_doc = sources[0]["document"]
    assert "Security Monitoring" in top_doc or "SIEM" in top_doc

def test_capital_of_france_out_of_kb_regression():
    res = retrieve_relevant_chunks("What is the capital of France?", top_k=4)
    assert res["is_out_of_scope"]
    
    rag_res = process_rag_query("What is the capital of France?")
    assert rag_res["inspector"]["out_of_scope"]
    assert len(rag_res["sources"]) == 0
    assert "does not contain sufficient information" in rag_res["answer"].lower() or "not in knowledge base" in rag_res["answer"].lower()
