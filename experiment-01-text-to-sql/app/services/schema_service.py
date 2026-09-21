"""
Database Schema Retrieval & Introspection Service
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

import sqlite3
from typing import Dict, List, Any
from app.database import get_db_path

def get_database_schema_info() -> Dict[str, Any]:
    """
    Introspects SQLite database tables, column names, data types,
    foreign key relationships, and row counts.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve all user tables (exclude sqlite system tables)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_tables = []
    for table_name in tables:
        # Get column info (cid, name, type, notnull, dflt_value, pk)
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns_raw = cursor.fetchall()
        columns = [
            {"name": col[1], "type": col[2], "is_primary_key": bool(col[5])}
            for col in columns_raw
        ]

        # Get foreign keys (id, seq, table, from, to, on_update, on_delete, match)
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        fk_raw = cursor.fetchall()
        foreign_keys = [
            {"from_column": fk[3], "to_table": fk[2], "to_column": fk[4]}
            for fk in fk_raw
        ]

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
        row_count = cursor.fetchone()[0]

        schema_tables.append({
            "table_name": table_name,
            "columns": columns,
            "foreign_keys": foreign_keys,
            "row_count": row_count
        })

    conn.close()
    return {
        "database": "university.db",
        "table_count": len(schema_tables),
        "tables": schema_tables
    }

def format_schema_for_prompt() -> str:
    """
    Formats the introspected database schema into a clean, structured
    DDL-style prompt context string for the LLM.
    """
    info = get_database_schema_info()
    formatted_lines = [
        "DATABASE SCHEMA CONTEXT (Target Dialect: SQLite):",
        "================================================"
    ]

    for table in info["tables"]:
        tname = table["table_name"]
        cols_str = ", ".join([f"{c['name']} ({c['type']})" for c in table["columns"]])
        formatted_lines.append(f"\nTable: {tname}")
        formatted_lines.append(f"  Columns: {cols_str}")
        
        if table["foreign_keys"]:
            fk_strs = [f"{fk['from_column']} -> {fk['to_table']}({fk['to_column']})" for fk in table["foreign_keys"]]
            formatted_lines.append(f"  Relationships: {', '.join(fk_strs)}")

    formatted_lines.append("\nRELATIONAL MAPPINGS:")
    formatted_lines.append("- students.department_id references departments.id")
    formatted_lines.append("- courses.department_id references departments.id")
    formatted_lines.append("- faculty.department_id references departments.id")
    formatted_lines.append("- enrollments.student_id references students.id")
    formatted_lines.append("- enrollments.course_id references courses.id")

    return "\n".join(formatted_lines)
