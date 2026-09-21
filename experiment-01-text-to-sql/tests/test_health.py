"""
Health Endpoint Tests
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
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
    assert data["database_connected"] is True
