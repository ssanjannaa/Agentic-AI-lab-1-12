"""
FastAPI Integration Tests
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_images_endpoint():
    response = client.get("/api/images")
    assert response.status_code == 200
    images = response.json()
    assert len(images) >= 4
    assert "image_id" in images[0]

def test_api_search_endpoint():
    response = client.post("/api/search", json={
        "query": "vpn aws cloud",
        "category_filter": "All",
        "top_k": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["results_count"] >= 1
    assert data["results"][0]["image"]["image_id"] == "IMG-NET-02"

def test_api_vqa_endpoint():
    response = client.post("/api/vqa", json={
        "image_id": "IMG-PII-03",
        "question": "What PII masking rules are applied?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "masking rules" in data["answer"].lower() or "pii" in data["answer"].lower()
    assert data["confidence_score"] >= 0.85
