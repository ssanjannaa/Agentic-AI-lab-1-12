"""
Visual QA Engine Unit Tests
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from app.schemas import VisualQARequest
from app.services.vqa_engine import VisualQAEngine

def test_vqa_soc_dashboard_question():
    engine = VisualQAEngine()
    req = VisualQARequest(
        image_id="IMG-SOC-01",
        question="What critical alerts and monitored endpoints are shown?"
    )
    res = engine.answer_question(req)

    assert res.image_id == "IMG-SOC-01"
    assert "3 critical" in res.answer or "1420" in res.answer
    assert res.confidence_score >= 0.90
    assert len(res.grounded_evidence) > 0

def test_vqa_invalid_image_id():
    engine = VisualQAEngine()
    req = VisualQARequest(image_id="NON-EXISTENT-IMG", question="What is this?")
    res = engine.answer_question(req)

    assert res.confidence_score == 0.0
    assert "not found" in res.answer
