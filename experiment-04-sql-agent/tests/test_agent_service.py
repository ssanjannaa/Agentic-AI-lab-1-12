"""
Integration Tests for Autonomous ReAct Agent Loop
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from app.services.agent_service import run_sql_agent

def test_salary_agent_query():
    res = run_sql_agent("Which department has the highest average employee salary, and how many employees work there?")
    assert res.success is True
    assert res.row_count > 0
    assert len(res.agent_trace) >= 3
    assert res.tool_counters.total_calls >= 3
    assert "Product Management" in res.final_answer or "highest" in res.final_answer.lower()
    assert "127,000" in res.final_answer

def test_project_budget_agent_query():
    res = run_sql_agent("Which active project has the largest budget and which department owns it?")
    assert res.success is True
    assert res.row_count > 0
    assert "Next-Gen Cloud Orchestration" in res.final_answer or "budget" in res.final_answer.lower()

def test_employee_hours_agent_query():
    res = run_sql_agent("Which employee is assigned the highest total project hours?")
    assert res.success is True
    assert res.row_count > 0
    assert "hours" in res.final_answer.lower()

def test_out_of_domain_agent_query():
    res = run_sql_agent("What is the current stock price of Apple?")
    assert res.success is False
    assert "Out-of-Domain" in res.final_answer

def test_max_iterations_guard():
    # Attempting to request 15 iterations MUST still be strictly capped at 8
    res = run_sql_agent("Which department has the highest average employee salary, and how many employees work there?", max_iterations=15)
    assert res.iterations_used <= 8
