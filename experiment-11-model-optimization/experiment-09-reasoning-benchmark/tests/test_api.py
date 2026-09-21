"""
FastAPI Integration Tests
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_tasks_endpoint():
    response = client.get("/api/benchmarks/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 3
    assert "task_id" in tasks[0]

def test_api_evaluate_endpoint():
    response = client.post("/api/benchmarks/evaluate", json={
        "task_id": "TASK-FIN-02"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "TASK-FIN-02"
    assert len(data["strategy_results"]) == 4
    assert data["benchmark_duration_ms"] > 0
