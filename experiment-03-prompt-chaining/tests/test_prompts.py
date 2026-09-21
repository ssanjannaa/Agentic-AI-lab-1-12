"""
Stage Prompt Template Unit Tests
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from app.prompts.analysis_prompt import render_analysis_prompt
from app.prompts.extraction_prompt import render_extraction_prompt
from app.prompts.draft_prompt import render_draft_prompt
from app.prompts.critique_prompt import render_critique_prompt
from app.prompts.refinement_prompt import render_refinement_prompt
from app.prompts.final_prompt import render_final_prompt

def test_prompt_renderers():
    doc = "Sample text for testing prompt templates."
    p1 = render_analysis_prompt(doc)
    assert doc in p1
    
    p2 = render_extraction_prompt(doc, '{"topic": "AI"}')
    assert "Stage 1 Analysis" in p2
    
    p3 = render_draft_prompt(doc, "{}", "{}", "executive", "medium")
    assert "TARGET STYLE: executive" in p3
    
    p4 = render_critique_prompt(doc, "{}", "Draft summary text")
    assert "Draft summary text" in p4
    
    p5 = render_refinement_prompt("Draft summary", '{"critique": "good"}', "{}")
    assert "Stage 4 Critique" in p5
    
    p6 = render_final_prompt("Refined summary", "{}", "{}")
    assert "Refined summary" in p6
