"""
Text Processing & Metrics Service
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)

Handles text validation, normalization, sentence splitting, and metrics calculation.
"""

import re
from typing import Dict, Any, List

def normalize_whitespace(text: str) -> str:
    """Normalizes multiple spaces and newlines."""
    if not text:
        return ""
    # Replace multiple blank lines with double newline, multiple spaces with single space
    lines = [line.strip() for line in text.splitlines()]
    clean = "\n".join([l for l in lines if l])
    return clean

def count_words(text: str) -> int:
    """Calculates word count."""
    if not text:
        return 0
    words = re.findall(r'\w+', text)
    return len(words)

def compute_quality_metrics(
    original_text: str,
    final_summary: str,
    key_points: List[str],
    important_terms: List[Dict[str, str]],
    total_time_ms: float
) -> Dict[str, Any]:
    """
    Computes compression ratio, word counts, and chain metrics.
    """
    orig_words = count_words(original_text)
    final_words = count_words(final_summary)

    if orig_words > 0:
        ratio = round((final_words / orig_words) * 100, 1)
        ratio_str = f"{ratio}% of original size"
    else:
        ratio_str = "0%"

    return {
        "original_word_count": orig_words,
        "final_word_count": final_words,
        "compression_ratio": ratio_str,
        "key_points_extracted": len(key_points),
        "important_terms_count": len(important_terms),
        "stages_completed": 6,
        "total_processing_time_ms": round(total_time_ms, 2)
    }
