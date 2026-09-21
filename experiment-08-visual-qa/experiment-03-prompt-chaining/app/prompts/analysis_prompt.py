"""
Stage 1: Document Analysis Prompt Definition
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

STAGE_1_ANALYSIS_PROMPT = """
You are an expert Document Analyst AI in an Agentic Summarization Pipeline.

TASK: Analyze the provided document text and produce a structured analysis.

DOCUMENT TEXT:
{document_text}

INSTRUCTIONS:
Provide a structured JSON response with the following fields:
- topic: Primary topic or core subject matter
- document_type: Category (e.g. Technical Report, Academic Article, Policy Guide)
- domain: Field/industry (e.g. Computer Science, Cybersecurity, Higher Education)
- complexity: Estimated complexity level (Low, Medium, High)
- word_count: Word count of original document
- key_sections: List of identified major sections or structural themes
"""

def render_analysis_prompt(document_text: str) -> str:
    return STAGE_1_ANALYSIS_PROMPT.format(document_text=document_text)
