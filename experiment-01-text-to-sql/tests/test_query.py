"""
Query Integration Tests (Using Mock LLM Provider)
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_top_students():
    payload = {"question": "Top 5 students by CGPA"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "students" in data["tables_used"]
    assert len(data["rows"]) == 5
    assert len(data["workflow"]) == 6
    assert data["workflow"][-1]["status"] == "completed"

def test_query_department_count():
    payload = {"question": "How many students are in Computer Science?"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["rows"][0][0] > 0

def test_query_unsafe_rejection():
    payload = {"question": "DROP TABLE students;"}
    response = client.post("/api/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Unsafe query rejection" in data["explanation"] or "Multiple" in data["explanation"]
