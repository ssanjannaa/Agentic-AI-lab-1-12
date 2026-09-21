"""
Dataset Curator Service
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
Loads and inspects instruction datasets for domain adaptation fine-tuning.
"""

import json
import os
from typing import List, Dict, Any
from app.config import settings

def _resolve_path(rel_path: str) -> str:
    if os.path.isabs(rel_path):
        return rel_path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, rel_path)

def load_jsonl_dataset(path: str) -> List[Dict[str, Any]]:
    resolved = _resolve_path(path)
    if not os.path.exists(resolved):
        from data.seed_dataset import generate_datasets
        generate_datasets(resolved)

    samples = []
    with open(resolved, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(json.loads(line))
    return samples

class DatasetCuratorService:
    def __init__(self):
        self.train_path = settings.TRAIN_DATASET_PATH
        self.val_path = settings.VAL_DATASET_PATH

    def get_dataset_stats(self) -> Dict[str, Any]:
        train_samples = load_jsonl_dataset(self.train_path)
        val_samples = load_jsonl_dataset(self.val_path)

        train_tokens = sum(len(s.get("output", "").split()) for s in train_samples) * 1.3
        val_tokens = sum(len(s.get("output", "").split()) for s in val_samples) * 1.3

        return {
            "train_samples_count": len(train_samples),
            "val_samples_count": len(val_samples),
            "estimated_train_tokens": int(train_tokens),
            "estimated_val_tokens": int(val_tokens),
            "domain": "Cybersecurity & IT Infrastructure Compliance"
        }
