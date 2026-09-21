"""
FastAPI Integration Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_stats_endpoint():
    response = client.get("/api/fine-tuning/dataset")
    assert response.status_code == 200
    stats = response.json()
    assert stats["train_samples_count"] >= 3

def test_api_train_endpoint():
    response = client.post("/api/fine-tuning/train", json={
        "lora_rank": 8,
        "lora_alpha": 16,
        "learning_rate": 0.01,
        "num_epochs": 2,
        "batch_size": 4
    })
    assert response.status_code == 200
    data = response.json()
    assert data["training_status"] == "COMPLETED"
    assert len(data["epoch_metrics"]) == 2
    assert data["trainable_parameter_count"] > 0
    assert data["parameter_change_norm"] > 0.0

def test_api_eval_endpoint():
    response = client.post("/api/fine-tuning/evaluate", json={
        "instruction": "What is the recommended NIST PQC key exchange algorithm?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "accuracy_improvement_percentage_points" in data
    assert "relative_improvement_percent" in data
    assert data["accuracy_improvement_percentage_points"] == round(data["finetuned_model_accuracy"] - data["base_model_accuracy"], 2)
