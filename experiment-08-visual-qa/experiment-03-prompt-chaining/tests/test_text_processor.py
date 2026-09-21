"""
Text Processor Unit Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from app.services.text_processor import normalize_whitespace, count_words, compute_quality_metrics

def test_normalize_whitespace():
    raw = "  Hello   world!  \n\n\n  This is a   test.  "
    clean = normalize_whitespace(raw)
    assert clean == "Hello   world!\nThis is a   test."

def test_count_words():
    assert count_words("Agentic AI workflows perform multi-step planning.") == 7

def test_compute_quality_metrics():
    metrics = compute_quality_metrics(
        original_text="Word " * 200,
        final_summary="Word " * 50,
        key_points=["Point 1", "Point 2"],
        important_terms=[{"term": "T1", "definition": "D1"}],
        total_time_ms=125.5
    )
    assert metrics["original_word_count"] == 200
    assert metrics["final_word_count"] == 50
    assert metrics["compression_ratio"] == "25.0% of original size"
    assert metrics["stages_completed"] == 6
