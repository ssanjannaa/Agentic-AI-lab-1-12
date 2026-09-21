"""
Unit Tests for Database Agent Tools
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from app.services.database_tools import list_tables, get_schema, check_query_syntax, execute_sql

def test_list_tables_tool():
    res = list_tables()
    assert res["tool"] == "list_tables"
    assert res["count"] == 4
    tables = res["tables"]
    assert "departments" in tables
    assert "employees" in tables
    assert "projects" in tables
    assert "employee_projects" in tables

def test_get_schema_tool():
    res = get_schema(["employees", "departments"])
    assert res["tool"] == "get_schema"
    assert res["table_count"] == 2
    t_names = [t["table_name"] for t in res["tables"]]
    assert "employees" in t_names
    assert "departments" in t_names

    emp_table = next(t for t in res["tables"] if t["table_name"] == "employees")
    col_names = [c["name"] for c in emp_table["columns"]]
    assert "name" in col_names
    assert "department_id" in col_names
    assert "salary" in col_names

def test_check_query_syntax_tool():
    valid_res = check_query_syntax("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5;")
    assert valid_res["is_safe"] is True

    invalid_res = check_query_syntax("DROP TABLE employees;")
    assert invalid_res["is_safe"] is False
    assert "prohibited" in invalid_res["error_reason"].lower() or "unsafe" in invalid_res["error_reason"].lower()

def test_execute_sql_tool():
    res = execute_sql("SELECT name, code FROM departments ORDER BY id ASC;")
    assert res["success"] is True
    assert res["row_count"] == 5
    assert "name" in res["columns"]
    assert "code" in res["columns"]
    assert res["rows"][0][0] == "Engineering"
