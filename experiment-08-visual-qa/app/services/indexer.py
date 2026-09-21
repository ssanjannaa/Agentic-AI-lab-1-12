"""
Image Catalog Indexer Service
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

import json
import os
from typing import List, Dict, Any, Optional
from app.config import settings

def _resolve_path(rel_path: str) -> str:
    if os.path.isabs(rel_path):
        return rel_path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, rel_path)

def load_image_catalog() -> List[Dict[str, Any]]:
    path = _resolve_path(settings.IMAGES_CATALOG_PATH)
    if not os.path.exists(path):
        from data.seed_images import generate_image_catalog
        generate_image_catalog(path)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_image_by_id(image_id: str) -> Optional[Dict[str, Any]]:
    catalog = load_image_catalog()
    for img in catalog:
        if img["image_id"] == image_id:
            return img
    return None
