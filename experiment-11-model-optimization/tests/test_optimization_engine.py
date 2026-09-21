"""
Optimization Engine Unit Tests
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

from app.schemas import OptimizationRequest
from app.services.optimization_engine import ModelOptimizationEngine

def test_run_optimization_benchmark():
    engine = ModelOptimizationEngine()
    req = OptimizationRequest(base_model_name="CyberSecurity-FP32-8B-Base", target_hardware="Intel Core i7 CPU")
    res = engine.run_optimization_benchmark(req)

    assert len(res.profiles) == 4
    assert res.file_size_reduction_champion is not None
    assert res.throughput_champion is not None
    assert "Optimization Synthesis" in res.optimization_synthesis
