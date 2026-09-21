"""
End-to-End Query Orchestration Service
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)

Executes the visible 6-step Agentic AI pipeline:
Question -> Schema Retrieval -> Prompt Build & SQL Generation -> Safety Validation -> DB Execution -> Explanation
"""

from typing import Dict, Any, List
from app.services.schema_service import get_database_schema_info
from app.services.sql_generator import generate_sql_from_question
from app.services.sql_validator import sanitize_and_validate_sql
from app.database import execute_read_only_query
from app.services.llm_service import get_llm_provider
from app.config import settings

def process_natural_language_query(user_question: str) -> Dict[str, Any]:
    """
    Executes the full Text-to-SQL workflow and records step-by-step pipeline execution details.
    """
    workflow_steps = []

    # Step 1: Understanding Question
    workflow_steps.append({
        "step": "Understanding Question",
        "status": "completed",
        "details": f"Received query: '{user_question}'"
    })

    # Step 2: Retrieving Schema Context
    schema_info = get_database_schema_info()
    table_names = [t["table_name"] for t in schema_info["tables"]]
    workflow_steps.append({
        "step": "Retrieving Schema",
        "status": "completed",
        "details": f"Retrieved schema context for {len(table_names)} tables: {', '.join(table_names)}"
    })

    # Step 3: Prompt Construction & SQL Query Generation
    llm_output = generate_sql_from_question(user_question)
    raw_sql = llm_output.get("generated_sql", "")
    reasoning = llm_output.get("reasoning_summary", "Generated query based on schema.")
    tables_used = llm_output.get("tables_used", [])

    workflow_steps.append({
        "step": "Generating SQL",
        "status": "completed",
        "sql": raw_sql,
        "details": reasoning
    })

    # Step 4: Server-Side SQL Safety Validation
    is_safe, error_reason, clean_sql = sanitize_and_validate_sql(raw_sql)
    if not is_safe:
        workflow_steps.append({
            "step": "Validating Query",
            "status": "failed",
            "safe": False,
            "details": error_reason
        })
        return {
            "question": user_question,
            "generated_sql": raw_sql,
            "columns": [],
            "rows": [],
            "explanation": f"⚠️ Query Execution Blocked: {error_reason}",
            "tables_used": tables_used,
            "reasoning_summary": reasoning,
            "workflow": workflow_steps,
            "provider": settings.LLM_PROVIDER,
            "success": False,
            "error": error_reason
        }

    workflow_steps.append({
        "step": "Validating Query",
        "status": "completed",
        "safe": True,
        "details": "Query passed server-side SELECT-only safety validation."
    })

    # Step 5: Read-Only Database Execution
    try:
        query_result = execute_read_only_query(clean_sql)
        columns = query_result["columns"]
        rows = query_result["rows"]
        row_count = query_result["row_count"]

        workflow_steps.append({
            "step": "Executing",
            "status": "completed",
            "row_count": row_count,
            "details": f"Executed against SQLite. Retrieved {row_count} row(s)."
        })
    except Exception as e:
        error_msg = f"Database Execution Error: {str(e)}"
        workflow_steps.append({
            "step": "Executing",
            "status": "failed",
            "details": error_msg
        })
        return {
            "question": user_question,
            "generated_sql": clean_sql,
            "columns": [],
            "rows": [],
            "explanation": f"❌ {error_msg}",
            "tables_used": tables_used,
            "reasoning_summary": reasoning,
            "workflow": workflow_steps,
            "provider": settings.LLM_PROVIDER,
            "success": False,
            "error": error_msg
        }

    # Step 6: Conversational Natural-Language Explanation
    provider = get_llm_provider()
    explanation = provider.generate_explanation(user_question, clean_sql, columns, rows)

    workflow_steps.append({
        "step": "Explaining Result",
        "status": "completed",
        "details": "Synthesized natural language summary."
    })

    return {
        "question": user_question,
        "generated_sql": clean_sql,
        "columns": columns,
        "rows": rows,
        "explanation": explanation,
        "tables_used": tables_used,
        "reasoning_summary": reasoning,
        "workflow": workflow_steps,
        "provider": settings.LLM_PROVIDER,
        "success": True,
        "error": None
    }
