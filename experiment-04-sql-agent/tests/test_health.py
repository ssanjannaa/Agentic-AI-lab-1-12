"""
API Health Endpoint Tests
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8003
    assert "Experiment 04" in data["app"]
    assert data["database_status"] == "connected"
