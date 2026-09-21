"""
Real LoRA Trainer Unit Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from app.schemas import FineTuningConfig
from app.services.trainer import RealLoRATrainer

def test_run_real_training_job():
    trainer = RealLoRATrainer()
    config = FineTuningConfig(lora_rank=8, lora_alpha=16, num_epochs=3, learning_rate=0.01)
    res = trainer.run_training_job(config)

    assert res.training_status == "COMPLETED"
    assert len(res.epoch_metrics) == 3
    assert res.trainable_parameter_count > 0
    assert res.frozen_parameter_count > 0
    assert res.parameter_change_norm > 0.0
    assert res.final_train_loss > 0
    assert res.final_perplexity > 0
