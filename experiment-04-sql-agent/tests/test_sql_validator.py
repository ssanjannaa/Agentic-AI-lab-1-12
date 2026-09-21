"""
Unit Tests for SQL Safety Validation Rules
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from app.services.sql_validator import sanitize_and_validate_sql

def test_valid_select_query():
    is_safe, error, cleaned = sanitize_and_validate_sql("SELECT * FROM employees WHERE salary > 100000;")
    assert is_safe is True
    assert error == ""
    assert cleaned == "SELECT * FROM employees WHERE salary > 100000"

def test_valid_with_clause_query():
    is_safe, error, cleaned = sanitize_and_validate_sql("WITH dept_avg AS (SELECT department_id, AVG(salary) as avg_sal FROM employees GROUP BY department_id) SELECT * FROM dept_avg;")
    assert is_safe is True
    assert error == ""

def test_valid_quoted_semicolon_and_forbidden_words():
    # Quoted forbidden keywords or semicolons inside string literals MUST be permitted
    is_safe1, err1, _ = sanitize_and_validate_sql("SELECT * FROM employees WHERE name = 'Alice; DROP TABLE employees;';")
    assert is_safe1 is True
    assert err1 == ""

    is_safe2, err2, _ = sanitize_and_validate_sql("SELECT 'DROP TABLE employees' AS harmless_text;")
    assert is_safe2 is True
    assert err2 == ""

    is_safe3, err3, _ = sanitize_and_validate_sql("SELECT 'INSERT UPDATE DELETE CREATE ALTER' AS harmless_text;")
    assert is_safe3 is True
    assert err3 == ""

    is_safe4, err4, _ = sanitize_and_validate_sql("SELECT * FROM projects WHERE name = 'CREATE';")
    assert is_safe4 is True
    assert err4 == ""

def test_blocked_drop_query():
    is_safe, error, _ = sanitize_and_validate_sql("DROP TABLE employees;")
    assert is_safe is False
    assert "prohibited" in error.lower() or "only select" in error.lower()

def test_blocked_delete_query():
    is_safe, error, _ = sanitize_and_validate_sql("DELETE FROM employees WHERE id = 1;")
    assert is_safe is False

def test_blocked_update_query():
    is_safe, error, _ = sanitize_and_validate_sql("UPDATE employees SET salary = 200000 WHERE id = 1;")
    assert is_safe is False

def test_blocked_multiple_statements():
    is_safe, error, _ = sanitize_and_validate_sql("SELECT * FROM employees; DROP TABLE departments;")
    assert is_safe is False
    assert "multiple" in error.lower()

def test_blocked_cte_with_write_operation():
    is_safe, error, _ = sanitize_and_validate_sql("WITH d AS (DELETE FROM employees RETURNING *) SELECT * FROM d;")
    assert is_safe is False
    assert "delete" in error.lower() or "prohibited" in error.lower()
