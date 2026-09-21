"""
FastAPI Health & System Metadata Unit Tests
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8011
    assert data["knowledge_base_documents"] >= 5
    assert data["sample_incidents_loaded"] >= 5

def test_system_metadata_endpoint():
    response = client.get("/api/system")
    assert response.status_code == 200
    data = response.json()
    assert data["port"] == 8011
    assert len(data["agents"]) == 7

def test_sample_incidents_endpoint():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert "id" in data[0]

def test_knowledge_stats_endpoint():
    response = client.get("/api/knowledge/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_documents"] >= 5
    assert data["total_indexed_chunks"] >= 5
