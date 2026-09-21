"""
Health Endpoint Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8009
    assert "Experiment 10" in data["app"]
    assert data["datasets_status"] == "loaded"
