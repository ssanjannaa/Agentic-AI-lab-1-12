"""
Summary Styles Unit Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from app.services.chain_service import execute_prompt_chain

sample_doc = (
    "Enterprise Cybersecurity Incident Response requires 6 distinct phases: Preparation, Identification, "
    "Containment, Eradication, Recovery, and Lessons Learned. SIEM log aggregation is essential."
)

def test_executive_summary_style():
    res = execute_prompt_chain(sample_doc, style="executive", length="medium")
    assert "executive" in res["draft_summary"].lower() or "executive" in res["final_summary"].lower()

def test_bullet_summary_style():
    res = execute_prompt_chain(sample_doc, style="bullet", length="medium")
    assert "•" in res["final_summary"] or "bullet" in res["final_summary"].lower()

def test_academic_summary_style():
    res = execute_prompt_chain(sample_doc, style="academic", length="medium")
    assert "academic" in res["draft_summary"].lower() or "study" in res["draft_summary"].lower()

def test_concise_summary_style():
    res = execute_prompt_chain(sample_doc, style="concise", length="medium")
    assert len(res["final_summary"]) > 0

def test_detailed_summary_style():
    res = execute_prompt_chain(sample_doc, style="detailed", length="medium")
    assert "detailed" in res["draft_summary"].lower() or "analysis" in res["draft_summary"].lower()
