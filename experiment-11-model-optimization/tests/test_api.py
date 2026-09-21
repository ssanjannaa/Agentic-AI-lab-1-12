"""
FastAPI Integration Tests
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_optimize_endpoint():
    response = client.post("/api/optimize", json={
        "base_model_name": "CyberSecurity-FP32-8B-Base",
        "target_hardware": "Intel Core i7 CPU"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["profiles"]) == 4
    assert data["file_size_reduction_champion"] is not None

def test_api_optimization_benchmark_endpoint():
    response = client.post("/api/optimization/benchmark", json={
        "base_model_name": "CyberSecurity-FP32-8B-Base",
        "target_hardware": "Intel Core i7 CPU"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["profiles"]) == 4
