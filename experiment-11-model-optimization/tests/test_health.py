"""
Health Endpoint Tests
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8010
    assert "Experiment 11" in data["app"]
    assert data["optimization_engine_status"] == "ready"
