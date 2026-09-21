"""
Health Endpoint Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8004
    assert "Experiment 05" in data["app"]
    assert data["leads_dataset_status"] == "loaded"
