"""
Model Evaluator Service Unit Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

import os
from app.schemas import EvalRequest, FineTuningConfig
from app.services.evaluator import ModelEvaluatorService
from app.services.trainer import RealLoRATrainer

def test_evaluate_models_comparison():
    evaluator = ModelEvaluatorService()
    req = EvalRequest(instruction="Explain how to mitigate CVE-2023-23397 Outlook vulnerability.")
    res = evaluator.evaluate_models(req)

    assert res.total_evaluated_samples == 10
    assert 0.0 <= res.base_model_accuracy <= 100.0
    assert 0.0 <= res.finetuned_model_accuracy <= 100.0
    assert 0 <= res.base_correct_count <= res.total_evaluated_samples
    assert 0 <= res.finetuned_correct_count <= res.total_evaluated_samples
    assert res.accuracy_improvement_percentage_points == round(res.finetuned_model_accuracy - res.base_model_accuracy, 2)
    assert "Base Un-adapted Model" in res.base_model_output
    assert "Fine-Tuned Domain Adapter" in res.finetuned_model_output

def test_canonical_reproducible_workflow_consistency():
    # 1. Clean previous checkpoint to test deterministic initialization
    checkpoint_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checkpoints")
    checkpoint_path = os.path.join(checkpoint_dir, "lora_adapter.pt")
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)

    # 2. Run canonical trainer job with default FineTuningConfig (epochs=5, lr=0.05, rank=8, alpha=16)
    canonical_config = FineTuningConfig()
    trainer = RealLoRATrainer()
    job_res = trainer.run_training_job(canonical_config)

    assert os.path.exists(job_res.checkpoint_path)

    # 3. Evaluate using ModelEvaluatorService
    evaluator = ModelEvaluatorService()
    eval_res = evaluator.evaluate_models(EvalRequest())

    # 4. Strict consistency assertions: UI/API trained metric == evaluation of saved/reloaded canonical checkpoint
    assert eval_res.total_evaluated_samples == 10
    assert eval_res.base_correct_count == 2
    assert eval_res.base_model_accuracy == 20.0
    assert eval_res.finetuned_correct_count == 4
    assert eval_res.finetuned_model_accuracy == 40.0
    assert eval_res.accuracy_improvement_percentage_points == 20.0
    assert eval_res.relative_improvement_percent == 100.0
    assert eval_res.accuracy_improvement_percentage_points == round(eval_res.finetuned_model_accuracy - eval_res.base_model_accuracy, 2)
