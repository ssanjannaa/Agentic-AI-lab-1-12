"""
Benchmark Engine Unit Tests
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
"""

from app.schemas import BenchmarkRequest
from app.services.benchmark_engine import ReasoningBenchmarkEngine

def test_benchmark_engine_run():
    engine = ReasoningBenchmarkEngine()
    req = BenchmarkRequest(task_id="TASK-CYBER-01")
    res = engine.run_benchmark(req)

    assert res.task_id == "TASK-CYBER-01"
    assert len(res.strategy_results) == 4
    assert res.winning_strategy_accuracy == "Multi-Agent Collaboration"
    assert res.winning_strategy_efficiency == "Direct Answer"
    assert "Benchmark Synthesis" in res.tradeoff_synthesis
