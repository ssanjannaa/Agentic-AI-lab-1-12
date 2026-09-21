"""
Stage 6: Final Structured Output Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_6_FINAL_PROMPT = """
You are the Final Output Compiler AI in an Agentic Summarization Pipeline.

TASK: Assemble the final polished summary package incorporating key points and terms.

REFINED SUMMARY (Stage 5):
{refined_summary}

EXTRACTED KEY INFO (Stage 2):
{extraction_json}

ANALYSIS METRICS (Stage 1):
{analysis_json}

INSTRUCTIONS:
Produce the final publication-ready summary package containing:
- final_summary: The polished refined text
- key_points: Standardized bullet list
- important_terms: Terms glossary
"""

def render_final_prompt(refined_summary: str, extraction_json: str, analysis_json: str) -> str:
    return STAGE_6_FINAL_PROMPT.format(
        refined_summary=refined_summary,
        extraction_json=extraction_json,
        analysis_json=analysis_json
    )
