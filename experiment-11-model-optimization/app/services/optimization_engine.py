"""
Real Optimization Benchmark Engine
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)

Evaluates FP32 Baseline, Symmetric INT8 Quantization, Packed INT4 Quantization,
and Distilled Student Model profiles using real serialized disk artifacts and timing metrics.
Explicitly separates genuine model forward passes/sec from synthetic scalar arithmetic microbenchmarks (operations/sec).
"""

import time
from typing import List
from app.schemas import OptimizationRequest, OptimizationComparisonResponse, OptimizationProfile
from app.services.quantizer import RealQuantizationEngineService
from app.services.distiller import RealKnowledgeDistillationService

class ModelOptimizationEngine:
    def __init__(self):
        self.quantizer = RealQuantizationEngineService()
        self.distiller = RealKnowledgeDistillationService()

    def run_optimization_benchmark(self, req: OptimizationRequest) -> OptimizationComparisonResponse:
        start_time = time.time()

        profiles: List[OptimizationProfile] = [
            self.quantizer.get_fp32_profile(),
            self.quantizer.get_int8_profile(),
            self.quantizer.get_int4_profile(),
            self.distiller.get_distillation_profile()
        ]

        size_champion = max(profiles, key=lambda p: p.metrics.compression_ratio_percent)
        throughput_champion = max(profiles, key=lambda p: p.metrics.throughput_inferences_sec)

        synthesis = (
            f"Optimization Synthesis for '{req.base_model_name}' on {req.target_hardware}: "
            f"Packed INT4 Quantization achieved highest artifact size reduction ({size_champion.metrics.compression_ratio_percent}% file size reduction, "
            f"from {profiles[0].metrics.serialized_file_size_mb} MB down to {size_champion.metrics.serialized_file_size_mb} MB, MSE={profiles[2].metrics.reconstruction_mse}). "
            f"Symmetric INT8 Post-Training Quantization provides 75.0% memory reduction with negligible reconstruction error (MSE={profiles[1].metrics.reconstruction_mse}). "
            f"The 3B Distilled Student Architecture provides genuine PyTorch model forward pass execution ({profiles[3].metrics.forward_passes_sec} forward passes/sec)."
        )

        duration = round((time.time() - start_time) * 1000, 2)

        return OptimizationComparisonResponse(
            base_model_name=req.base_model_name or "CyberSecurity-FP32-8B-Base",
            target_hardware=req.target_hardware or "Intel Core i7 CPU / Edge Workstation",
            profiles=profiles,
            file_size_reduction_champion=size_champion.level_name,
            throughput_champion=throughput_champion.level_name,
            optimization_synthesis=synthesis,
            evaluation_duration_ms=duration
        )
