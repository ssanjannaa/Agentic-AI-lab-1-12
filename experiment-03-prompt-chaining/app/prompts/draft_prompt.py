"""
Stage 3: Draft Summary Generation Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_3_DRAFT_PROMPT = """
You are a First-Pass Summary Author AI in an Agentic Summarization Pipeline.

TASK: Generate a first-pass draft summary based on the extracted key information, analysis, requested style, and requested length.

TARGET STYLE: {summary_style}
TARGET LENGTH: {summary_length}

STAGE 1 ANALYSIS:
{analysis_json}

STAGE 2 EXTRACTED KEY INFORMATION:
{extraction_json}

ORIGINAL DOCUMENT:
{document_text}

INSTRUCTIONS:
Generate a coherent draft summary matching the target style ({summary_style}) and length ({summary_length}). This is a first-pass draft that will be critiqued in Stage 4.
"""

def render_draft_prompt(document_text: str, analysis_json: str, extraction_json: str, summary_style: str, summary_length: str) -> str:
    return STAGE_3_DRAFT_PROMPT.format(
        document_text=document_text,
        analysis_json=analysis_json,
        extraction_json=extraction_json,
        summary_style=summary_style,
        summary_length=summary_length
    )
