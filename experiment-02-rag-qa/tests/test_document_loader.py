"""
Document Loader Unit Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.document_loader import load_knowledge_base_documents

def test_load_knowledge_base_documents():
    docs = load_knowledge_base_documents()
    assert len(docs) == 9
    
    titles = [d.title for d in docs]
    assert "Network Security Fundamentals" in titles
    assert "Phishing and Social Engineering" in titles
    assert "Malware and Ransomware" in titles
