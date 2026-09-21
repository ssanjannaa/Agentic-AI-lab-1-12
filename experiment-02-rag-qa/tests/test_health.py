"""
Health & Status Endpoint Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["course"] == "MR23-1CS0436"
    assert "llm_provider" in data

def test_kb_status_endpoint():
    response = client.get("/api/knowledge-base/status")
    assert response.status_code == 200
    data = response.json()
    assert data["documents_indexed"] == 9
    assert data["chunks_indexed"] >= 30
