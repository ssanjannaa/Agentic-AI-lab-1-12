"""
Agent Database Tools Implementation
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)

Implements the four core agent tools:
1. list_tables
2. get_schema
3. check_query_syntax
4. execute_sql
"""

import sqlite3
from typing import Dict, List, Any, Optional
from app.database import get_db_path, execute_read_only_query
from app.services.sql_validator import sanitize_and_validate_sql

PERMITTED_TABLES = ["departments", "employees", "projects", "employee_projects"]

def list_tables() -> Dict[str, Any]:
    """
    Tool 1: list_tables
    Returns all permitted user tables in company.db. Excludes sqlite internal tables.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    all_tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Filter to permitted tables
    valid_tables = [t for t in all_tables if t in PERMITTED_TABLES]
    return {
        "tool": "list_tables",
        "tables": valid_tables,
        "count": len(valid_tables)
    }

def get_schema(tables: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Tool 2: get_schema
    Inspects columns, data types, primary keys, foreign keys, and row counts for specified tables.
    If tables is None or empty, returns schema for all permitted tables.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if not tables:
        target_tables = PERMITTED_TABLES
    else:
        target_tables = [t.strip() for t in tables if t.strip() in PERMITTED_TABLES]

    schema_tables = []
    for tname in target_tables:
        cursor.execute(f"PRAGMA table_info('{tname}');")
        columns_raw = cursor.fetchall()
        columns = [
            {"name": col[1], "type": col[2], "is_primary_key": bool(col[5])}
            for col in columns_raw
        ]

        cursor.execute(f"PRAGMA foreign_key_list('{tname}');")
        fk_raw = cursor.fetchall()
        foreign_keys = [
            {"from_column": fk[3], "to_table": fk[2], "to_column": fk[4]}
            for fk in fk_raw
        ]

        cursor.execute(f"SELECT COUNT(*) FROM '{tname}';")
        row_count = cursor.fetchone()[0]

        schema_tables.append({
            "table_name": tname,
            "columns": columns,
            "foreign_keys": foreign_keys,
            "row_count": row_count
        })

    conn.close()

    return {
        "tool": "get_schema",
        "database": "company.db",
        "table_count": len(schema_tables),
        "tables": schema_tables
    }

def check_query_syntax(sql_query: str) -> Dict[str, Any]:
    """
    Tool 3: check_query_syntax
    Validates an SQL query string for read-only compliance and basic structure before execution.
    """
    is_safe, error_reason, cleaned_sql = sanitize_and_validate_sql(sql_query)
    return {
        "tool": "check_query_syntax",
        "is_safe": is_safe,
        "error_reason": error_reason,
        "cleaned_sql": cleaned_sql
    }

def execute_sql(sql_query: str) -> Dict[str, Any]:
    """
    Tool 4: execute_sql
    Validates and executes a read-only SELECT query against company.db.
    Returns column names, rows, row count, and execution status/errors.
    """
    # 1. First run safety validation
    is_safe, error_reason, cleaned_sql = sanitize_and_validate_sql(sql_query)
    if not is_safe:
        return {
            "tool": "execute_sql",
            "success": False,
            "error": f"Validation Failed: {error_reason}",
            "sql": sql_query,
            "columns": [],
            "rows": [],
            "row_count": 0
        }

    # 2. Execute on SQLite database
    try:
        query_result = execute_read_only_query(cleaned_sql)
        return {
            "tool": "execute_sql",
            "success": True,
            "error": None,
            "sql": cleaned_sql,
            "columns": query_result["columns"],
            "rows": query_result["rows"],
            "row_count": query_result["row_count"]
        }
    except Exception as e:
        return {
            "tool": "execute_sql",
            "success": False,
            "error": f"Database Execution Error: {str(e)}",
            "sql": cleaned_sql,
            "columns": [],
            "rows": [],
            "row_count": 0
        }
