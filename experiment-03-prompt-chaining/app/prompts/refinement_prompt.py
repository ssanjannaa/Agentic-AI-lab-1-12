"""
Stage 5: Summary Refinement Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_5_REFINEMENT_PROMPT = """
You are a Master Editor AI in an Agentic Summarization Pipeline.

TASK: Refine and rewrite the Stage 3 Draft Summary by incorporating Stage 4 Critique feedback and Stage 2 Key Information.

STAGE 3 DRAFT SUMMARY:
{draft_summary}

STAGE 4 CRITIQUE & RECOMMENDATIONS:
{critique_json}

STAGE 2 KEY INFORMATION:
{extraction_json}

INSTRUCTIONS:
Produce a polished, refined summary resolving all critique points, eliminating redundancies, and ensuring complete alignment with the requested style and length.
"""

def render_refinement_prompt(draft_summary: str, critique_json: str, extraction_json: str) -> str:
    return STAGE_5_REFINEMENT_PROMPT.format(
        draft_summary=draft_summary,
        critique_json=critique_json,
        extraction_json=extraction_json
    )
