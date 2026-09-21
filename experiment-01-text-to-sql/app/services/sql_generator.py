"""
SQL Prompt Assembly & Generation Service
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

from typing import Dict, Any
from app.services.schema_service import format_schema_for_prompt
from app.services.llm_service import get_llm_provider

SYSTEM_PROMPT_TEMPLATE = """
You are an expert Text-to-SQL AI Assistant for a University Database Management System.
Your job is to translate user natural language questions into valid, syntactically correct SQLite SELECT queries based ONLY on the provided schema.

{schema_context}

STRICT SQL RULES:
1. Generate ONLY SELECT statements or WITH CTE clauses leading to SELECT.
2. DO NOT generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or PRAGMA statements.
3. Use SQLite compatible syntax (e.g. strftime for dates, GROUP BY for aggregations, LIMIT for top-N).
4. Do NOT hallucinate tables or columns that are not present in the schema context.
5. Use table aliases (e.g. s for students, d for departments, c for courses, e for enrollments, f for faculty).

REQUIRED OUTPUT FORMAT:
You MUST respond strictly with a valid JSON object matching this schema:
{{
  "generated_sql": "SELECT ...;",
  "reasoning_summary": "A concise 1-sentence explanation of query logic.",
  "tables_used": ["table1", "table2"]
}}
"""

def generate_sql_from_question(user_question: str) -> Dict[str, Any]:
    """
    Constructs schema context prompt, invokes active LLM provider,
    and returns parsed SQL response dictionary.
    """
    schema_context = format_schema_for_prompt()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema_context=schema_context)
    
    provider = get_llm_provider()
    response = provider.generate_sql_response(system_prompt, user_question)
    return response
