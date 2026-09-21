"""
SQL Safety Validation Unit Tests
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

from app.services.sql_validator import sanitize_and_validate_sql

def test_valid_select_queries():
    valid_queries = [
        "SELECT * FROM students;",
        "SELECT name, cgpa FROM students WHERE cgpa > 8.5 ORDER BY cgpa DESC;",
        "WITH cs_students AS (SELECT * FROM students WHERE department_id = 1) SELECT * FROM cs_students;",
        "```sql\nSELECT COUNT(*) FROM courses;\n```"
    ]
    for q in valid_queries:
        is_safe, error, clean_sql = sanitize_and_validate_sql(q)
        assert is_safe is True, f"Failed for valid query: {q}. Error: {error}"
        assert error == ""
        assert clean_sql.upper().startswith("SELECT") or clean_sql.upper().startswith("WITH")

def test_reject_destructive_queries():
    destructive_queries = [
        "DELETE FROM students;",
        "DROP TABLE departments;",
        "UPDATE students SET cgpa = 10.0 WHERE id = 1;",
        "INSERT INTO departments (name, code) VALUES ('Hacking', 'HACK');",
        "ALTER TABLE students ADD COLUMN password TEXT;",
        "TRUNCATE TABLE enrollments;",
        "CREATE TABLE malicious (id INT);"
    ]
    for q in destructive_queries:
        is_safe, error, clean_sql = sanitize_and_validate_sql(q)
        assert is_safe is False, f"Should have rejected query: {q}"
        assert "Unsafe query rejection" in error or "prohibited" in error

def test_reject_multiple_statements():
    multi_queries = [
        "SELECT * FROM students; DROP TABLE students;",
        "SELECT * FROM courses; DELETE FROM faculty;"
    ]
    for q in multi_queries:
        is_safe, error, clean_sql = sanitize_and_validate_sql(q)
        assert is_safe is False, f"Should have rejected multiple statements in: {q}"
        assert "Multiple SQL statements detected" in error or "Unsafe query rejection" in error
