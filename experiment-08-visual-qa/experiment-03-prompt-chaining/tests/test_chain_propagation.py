"""
CRITICAL: Chain Context Propagation Unit Test
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)

Proves that each stage in the 6-stage chain explicitly receives and consumes
structured outputs from preceding stages.
"""

from app.services.chain_service import execute_prompt_chain
from app.services.llm_service import OfflineSummarizationProvider

def test_chain_context_propagation():
    sample_text = (
        "Zero Trust Architecture (ZTA) fundamentally replaces implicit trust with explicit verification. "
        "Key pillars include Continuous Authentication, Least Privilege Access Control, and Micro-segmentation."
    )
    
    res = execute_prompt_chain(sample_text, style="executive", length="medium")
    
    assert res["success"] is True
    chain_trace = res["chain_trace"]
    assert len(chain_trace) == 6
    
    # 1. Verify Stage 1 Document Analysis output fed into Stage 2 inputs
    stg2_inputs = chain_trace[1]["inputs_consumed"]
    assert "Stage 1 Document Analysis" in stg2_inputs
    
    # 2. Verify Stage 2 Extracted Info fed into Stage 3 Draft Summary inputs
    stg3_inputs = chain_trace[2]["inputs_consumed"]
    assert "Stage 2 Extracted Info" in stg3_inputs
    
    # 3. Verify Stage 3 Draft Summary fed into Stage 4 Critique inputs
    stg4_inputs = chain_trace[3]["inputs_consumed"]
    assert "Stage 3 Draft Summary" in stg4_inputs
    
    # 4. Verify Stage 4 Critique Feedback fed into Stage 5 Refinement inputs
    stg5_inputs = chain_trace[4]["inputs_consumed"]
    assert "Stage 4 Critique Feedback" in stg5_inputs
    
    # 5. Verify Stage 5 Refinement fed into Stage 6 Final Output
    stg6_inputs = chain_trace[5]["inputs_consumed"]
    assert "Stage 5 Refined Summary" in stg6_inputs
