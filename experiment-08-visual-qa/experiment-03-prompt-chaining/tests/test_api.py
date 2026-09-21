"""
FastAPI Summarize Endpoint Integration Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_sample_fetching():
    response = client.get("/api/samples?id=01_agentic_ai_paradigms")
    assert response.status_code == 200
    data = response.json()
    assert "Agentic AI" in data["title"]
    assert len(data["content"]) > 100

def test_api_summarize_success():
    payload = {
        "text": "Agentic AI systems possess autonomous planning, decision-making, tool execution, memory reflection, and multi-agent coordination capabilities.",
        "summary_style": "executive",
        "summary_length": "medium"
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["chain_trace"]) == 6
    assert data["metrics"]["stages_completed"] == 6

def test_api_summarize_short_text_rejection():
    payload = {"text": "Too short"}
    response = client.post("/api/summarize", json=payload)
    assert response.status_code in (400, 422)
    data = response.json()
    assert "too_short" in str(data["detail"]).lower() or "at least 30" in str(data["detail"]).lower() or "too short" in str(data["detail"]).lower()
