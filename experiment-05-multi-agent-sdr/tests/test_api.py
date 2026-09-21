"""
FastAPI Endpoints Integration Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_leads_endpoint():
    response = client.get("/api/leads")
    assert response.status_code == 200
    leads = response.json()
    assert len(leads) >= 6
    assert "company_name" in leads[0]

def test_api_campaign_endpoint():
    response = client.post("/api/sdr/campaign", json={
        "target_industry": "All",
        "target_region": "All",
        "min_qualification_threshold": 60,
        "value_proposition": "Enterprise Agentic Platform"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["leads_discovered_count"] >= 6
    assert data["leads_qualified_count"] >= 1
    assert len(data["agent_traces"]) == 5
