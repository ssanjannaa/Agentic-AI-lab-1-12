"""
API Endpoint Integration Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_phishing_api():
    payload = {"question": "What is phishing?", "top_k": 4}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["sources"]) > 0
    assert "phishing" in data["answer"].lower()
    assert len(data["workflow"]) == 6

def test_query_out_of_kb_api():
    payload = {"question": "What is the capital of France?"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["sources"]) == 0
    assert data["inspector"]["out_of_scope"] is True

def test_rebuild_index_api():
    response = client.post("/api/index", json={"force_rebuild": True})
    assert response.status_code == 200
    data = response.json()
    assert data["documents_indexed"] == 9
    assert data["chunks_indexed"] >= 30
