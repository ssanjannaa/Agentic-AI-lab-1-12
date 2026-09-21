"""
Integration Tests for FastAPI API Endpoints
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_database_tables():
    response = client.get("/api/database/tables")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 4
    assert "employees" in data["tables"]

def test_api_database_schema():
    response = client.get("/api/database/schema")
    assert response.status_code == 200
    data = response.json()
    assert data["database"] == "company.db"
    assert data["table_count"] == 4

def test_api_database_validate_valid():
    response = client.post("/api/database/validate", json={"sql_query": "SELECT * FROM departments;"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_safe"] is True

def test_api_database_validate_invalid():
    response = client.post("/api/database/validate", json={"sql_query": "DROP TABLE departments;"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_safe"] is False

def test_api_agent_query_endpoint():
    response = client.post("/api/agent/query", json={
        "question": "Which active project has the largest budget and which department owns it?",
        "max_iterations": 8
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["row_count"] > 0
    assert len(data["agent_trace"]) >= 2
