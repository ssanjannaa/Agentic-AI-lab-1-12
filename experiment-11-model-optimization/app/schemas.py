"""
Pydantic API Request/Response Schemas
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OptimizationMetrics(BaseModel):
    serialized_file_size_mb: float
    compression_ratio_percent: float
    vram_usage_gb: float
    measured_latency_ms: float
    forward_passes_sec: float = Field(default=0.0, description="Genuine model forward passes / sec timing")
    synthetic_operations_sec: Optional[float] = Field(default=None, description="Synthetic scalar arithmetic microbenchmark timing")
    reconstruction_mse: float = 0.0

    @property
    def throughput_inferences_sec(self) -> float:
        return self.forward_passes_sec or (self.synthetic_operations_sec or 0.0)

    @property
    def throughput_tokens_sec(self) -> float:
        return self.throughput_inferences_sec

class OptimizationProfile(BaseModel):
    level_name: str  # "FP32 Baseline", "Symmetric INT8 Weight Quantization", "Packed INT4 Uniform Quantization", "3B Distilled Student Architecture"
    technique: str
    description: str
    artifact_path: str
    metrics: OptimizationMetrics

class OptimizationRequest(BaseModel):
    base_model_name: Optional[str] = Field(default="CyberSecurity-FP32-8B-Base", description="Base foundation model name")
    target_hardware: Optional[str] = Field(default="Intel Core i7 CPU / Edge Workstation", description="Target deployment hardware")

class OptimizationComparisonResponse(BaseModel):
    base_model_name: str
    target_hardware: str
    profiles: List[OptimizationProfile]
    file_size_reduction_champion: str
    throughput_champion: str
    optimization_synthesis: str
    evaluation_duration_ms: float
