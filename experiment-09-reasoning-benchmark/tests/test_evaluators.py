"""
Strategy Evaluators Unit Tests
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
"""

from app.schemas import BenchmarkTask
from app.services.zero_shot import ZeroShotEvaluator
from app.services.cot import ChainOfThoughtEvaluator
from app.services.react import ReActEvaluator
from app.services.multi_agent import MultiAgentEvaluator

def test_strategy_evaluators():
    task = BenchmarkTask(
        task_id="TASK-CYBER-01",
        title="SOC Incident Analysis",
        domain="Cybersecurity",
        complexity="High",
        problem_statement="Investigate CVE-2023-23397 exploitation.",
        ground_truth_key_factors=["CVE-2023-23397", "Containment"]
    )

    zs_res = ZeroShotEvaluator().evaluate(task)
    cot_res = ChainOfThoughtEvaluator().evaluate(task)
    react_res = ReActEvaluator().evaluate(task)
    ma_res = MultiAgentEvaluator().evaluate(task)

    assert zs_res.metrics.tool_invocations_count == 0
    assert cot_res.metrics.correctness_score > zs_res.metrics.correctness_score
    assert react_res.metrics.tool_invocations_count == 2
    assert ma_res.metrics.correctness_score >= 98
