"""
Stage 2: Key Information Extraction Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_2_EXTRACTION_PROMPT = """
You are an Information Extraction Specialist AI in an Agentic Summarization Pipeline.

TASK: Extract core factual information from the document, informed by the Stage 1 Analysis.

STAGE 1 ANALYSIS:
{analysis_json}

ORIGINAL DOCUMENT:
{document_text}

INSTRUCTIONS:
Extract and return structured JSON containing:
- key_points: Bullet list of primary points and key assertions
- core_concepts: Key technical or domain concepts introduced
- important_terms: Glossary list of important terms/abbreviations
- findings_and_conclusions: Summary of primary conclusions or recommendations
"""

def render_extraction_prompt(document_text: str, analysis_json: str) -> str:
    return STAGE_2_EXTRACTION_PROMPT.format(document_text=document_text, analysis_json=analysis_json)
