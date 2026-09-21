"""
Schema Introspection Tests
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_schema_endpoint():
    response = client.get("/api/schema")
    assert response.status_code == 200
    data = response.json()
    assert data["table_count"] == 5
    
    table_names = [t["table_name"] for t in data["tables"]]
    expected_tables = ["departments", "students", "courses", "enrollments", "faculty"]
    for t in expected_tables:
        assert t in table_names
