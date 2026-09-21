"""
Health Endpoint Tests
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["port"] == 8007
    assert "Experiment 08" in data["app"]
    assert data["catalog_status"] == "loaded"
