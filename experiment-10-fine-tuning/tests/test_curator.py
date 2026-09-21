"""
Dataset Curator Unit Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from app.services.dataset_curator import DatasetCuratorService, load_jsonl_dataset

def test_load_jsonl_dataset():
    samples = load_jsonl_dataset("data/train_dataset.jsonl")
    assert len(samples) >= 3
    assert "instruction" in samples[0]

def test_dataset_curator_stats():
    curator = DatasetCuratorService()
    stats = curator.get_dataset_stats()

    assert stats["train_samples_count"] >= 3
    assert stats["val_samples_count"] >= 1
    assert stats["estimated_train_tokens"] > 0
