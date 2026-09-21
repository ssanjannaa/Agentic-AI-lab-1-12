"""
Health & Modes Endpoint Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
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

def test_modes_endpoint():
    response = client.get("/api/modes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["styles"]) == 5
    assert len(data["lengths"]) == 3
