"""
Token-Based Read-Only SQL Security Validator
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)

Enforces strict READ-ONLY SELECT-only database execution rules using quote-aware lexical parsing and regex token matching.
Replaces string literals before tokenizing so forbidden keywords inside quoted strings do not cause false positives.
Does NOT claim or perform AST parsing.
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
    Ignores string literals when searching for executable forbidden keywords or semicolons.
    
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

    # 2. Strip single/double quoted string literals to analyze executable SQL structure
    outside_quotes = re.sub(r"'[^']*'|\"[^\"]*\"", " '' ", cleaned)

    # 3. Check for multiple statements (semicolon outside string literals)
    if ";" in outside_quotes:
        return False, "Multiple SQL statements detected. Only single-statement queries are allowed.", cleaned

    # 4. Check leading SELECT or WITH on executable text structure
    upper_executable = outside_quotes.upper().strip()
    if not (upper_executable.startswith("SELECT") or upper_executable.startswith("WITH")):
        return False, "Unsafe query rejection: Only SELECT queries are permitted.", cleaned

    # 5. Check for forbidden destructive keywords in executable tokens only
    tokens = re.findall(r'\b[A-Z_]+\b', upper_executable)
    for kw in FORBIDDEN_KEYWORDS:
        if kw in tokens:
            return False, f"Unsafe query rejection: Command '{kw}' is prohibited in read-only mode.", cleaned

    return True, "", cleaned
