"""
SQL Safety & Validation Engine
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)

Enforces strict READ-ONLY SELECT-only database execution rules.
"""

import re
from typing import Tuple

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", 
    "CREATE", "REPLACE", "ATTACH", "DETACH", "PRAGMA", "EXEC", 
    "EXECUTE", "GRANT", "REVOKE", "VACUUM", "REINDEX"
]

def sanitize_and_validate_sql(sql_query: str) -> Tuple[bool, str, str]:
    """
    Validates a generated SQL query string for security and read-only compliance.
    
    Returns:
        (is_safe: bool, error_message: str, cleaned_sql: str)
    """
    if not sql_query or not sql_query.strip():
        return False, "Query string is empty.", ""

    # 1. Clean query string (strip markdown block wrappers if present)
    cleaned = sql_query.strip()
    if cleaned.startswith("```sql"):
        cleaned = cleaned[6:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Trim trailing semicolon if present
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()

    # 2. Check for multiple statements (semicolon injection attempt)
    # Check if semicolons exist outside single/double quoted string literals
    outside_quotes = re.sub(r"'[^']*'|\"[^\"]*\"", "", cleaned)
    if ";" in outside_quotes:
        return False, "Multiple SQL statements detected. Only single-statement queries are allowed.", cleaned

    # 3. Check for leading SELECT or WITH
    upper_query = cleaned.upper().strip()
    if not (upper_query.startswith("SELECT") or upper_query.startswith("WITH")):
        return False, "Unsafe query rejection: Only SELECT queries are permitted.", cleaned

    # 4. Check for forbidden destructive keywords
    tokens = re.findall(r'\b[A-Z_]+\b', upper_query)
    for kw in FORBIDDEN_KEYWORDS:
        if kw in tokens:
            return False, f"Unsafe query rejection: Command '{kw}' is prohibited in read-only mode.", cleaned

    return True, "", cleaned
