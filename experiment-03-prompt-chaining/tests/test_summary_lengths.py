"""
Summary Lengths Unit Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from app.services.chain_service import execute_prompt_chain

sample_doc = (
    "Generative AI tools and adaptive tutoring algorithms in higher education create opportunities for personalized student learning. "
    "However, institutions must balance technical innovation with academic integrity, data privacy protection, and ethical evaluation standards."
)

def test_short_summary_length():
    res_short = execute_prompt_chain(sample_doc, style="executive", length="short")
    assert len(res_short["final_summary"]) <= 350

def test_long_summary_length():
    res_long = execute_prompt_chain(sample_doc, style="executive", length="long")
    res_short = execute_prompt_chain(sample_doc, style="executive", length="short")
    assert len(res_long["final_summary"]) >= len(res_short["final_summary"])
