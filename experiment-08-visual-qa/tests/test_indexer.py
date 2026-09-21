"""
Indexer Service Unit Tests
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from app.services.indexer import load_image_catalog, get_image_by_id

def test_load_image_catalog():
    catalog = load_image_catalog()
    assert len(catalog) >= 4
    ids = [i["image_id"] for i in catalog]
    assert "IMG-SOC-01" in ids
    assert "IMG-NET-02" in ids

def test_get_image_by_id():
    img = get_image_by_id("IMG-SOC-01")
    assert img is not None
    assert img["title"] == "SOC Incident Response Operations Dashboard"
    assert "dashboard" in img["labels"]
