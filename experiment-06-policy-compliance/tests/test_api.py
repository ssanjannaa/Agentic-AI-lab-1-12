"""
FastAPI Integration Tests
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_policies_endpoint():
    response = client.get("/api/policies")
    assert response.status_code == 200
    policies = response.json()
    assert len(policies) >= 3
    assert "policy_id" in policies[0]

def test_api_scenarios_endpoint():
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) >= 3
    assert "scenario_id" in scenarios[0]

def test_api_audit_endpoint():
    response = client.post("/api/compliance/audit", json={
        "policy_id": "POL-AI-03",
        "scenario_text": "An engineer uploaded production database credentials to a public AI chatbot."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["policy_id"] == "POL-AI-03"
    assert data["overall_status"] == "NON_COMPLIANT"
    assert len(data["recommended_remediations"]) > 0
