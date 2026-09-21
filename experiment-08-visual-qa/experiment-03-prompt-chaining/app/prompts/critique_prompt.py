"""
Stage 4: Summary Critique Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_4_CRITIQUE_PROMPT = """
You are an Auditor and Quality Critic AI in an Agentic Summarization Pipeline.

TASK: Critique the Stage 3 Draft Summary against the original document and Stage 2 Extracted Information.

STAGE 2 EXTRACTED KEY INFORMATION:
{extraction_json}

STAGE 3 DRAFT SUMMARY:
{draft_summary}

ORIGINAL DOCUMENT:
{document_text}

INSTRUCTIONS:
Evaluate the draft summary and return structured critique JSON:
- factual_coverage: Is key factual information accurately represented?
- missing_elements: What important key points were omitted?
- redundancy: Is there unnecessary wordiness or repetition?
- style_compliance: Does it match the requested style and length?
- refinement_recommendations: Specific action items to improve the summary in Stage 5.
"""

def render_critique_prompt(document_text: str, extraction_json: str, draft_summary: str) -> str:
    return STAGE_4_CRITIQUE_PROMPT.format(
        document_text=document_text,
        extraction_json=extraction_json,
        draft_summary=draft_summary
    )
