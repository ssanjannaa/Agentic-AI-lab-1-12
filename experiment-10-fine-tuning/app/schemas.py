"""
Pydantic API Request/Response Schemas
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class InstructionSample(BaseModel):
    instruction: str
    input: Optional[str] = ""
    output: str
    domain_label: Optional[int] = 0

class FineTuningConfig(BaseModel):
    lora_rank: int = Field(default=8, ge=2, le=64, description="LoRA rank adaptation dimension")
    lora_alpha: int = Field(default=16, ge=4, le=128, description="LoRA scaling factor")
    learning_rate: float = Field(default=0.05, ge=1e-5, le=1e-1, description="Learning rate")
    num_epochs: int = Field(default=5, ge=1, le=20, description="Training epochs count")
    batch_size: int = Field(default=4, ge=1, le=32, description="Batch size")

class EpochMetric(BaseModel):
    epoch: int
    train_loss: float
    val_loss: float
    perplexity: float
    duration_ms: float

class TrainingJobResponse(BaseModel):
    job_id: str
    model_name: str
    base_model_identifier: str
    lora_rank: int
    lora_alpha: int
    total_train_samples: int
    total_val_samples: int
    trainable_parameter_count: int
    frozen_parameter_count: int
    parameter_change_norm: float
    checkpoint_path: str
    epoch_metrics: List[EpochMetric]
    final_train_loss: float
    final_val_loss: float
    final_perplexity: float
    training_status: str  # "COMPLETED"
    total_training_duration_ms: float

class EvalRequest(BaseModel):
    instruction: Optional[str] = Field(
        default="Explain how to mitigate CVE-2023-23397 Outlook vulnerability in an enterprise environment.",
        description="Instruction or technical query to evaluate models against"
    )
    context_input: Optional[str] = Field(
        default="System environment: Windows Server 2019, Microsoft 365 Hybrid.",
        description="Optional technical context input"
    )

class ModelEvalResponse(BaseModel):
    instruction: str
    context_input: str
    total_evaluated_samples: int
    base_model_output: str
    base_correct_count: int
    base_model_accuracy: float  # Computed percentage (0-100)
    finetuned_model_output: str
    finetuned_correct_count: int
    finetuned_model_accuracy: float  # Computed percentage (0-100)
    accuracy_improvement_percentage_points: float  # Absolute percentage points difference (e.g. +20.0 percentage points)
    relative_improvement_percent: float  # Relative % change: ((finetuned - base) / base) * 100
    evaluation_duration_ms: float

    @property
    def accuracy_improvement_percent(self) -> float:
        return self.accuracy_improvement_percentage_points
