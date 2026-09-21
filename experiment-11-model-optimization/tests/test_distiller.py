"""
PyTorch Distillation Engine Unit Tests
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

import os
import torch
from app.services.distiller import RealKnowledgeDistillationService, StudentPyTorchModel

def test_distillation_profile_and_pytorch_training():
    distiller = RealKnowledgeDistillationService()
    profile = distiller.get_distillation_profile()

    assert os.path.exists(profile.artifact_path)
    assert profile.metrics.serialized_file_size_mb > 0
    assert profile.metrics.compression_ratio_percent > 0.0
    assert profile.metrics.forward_passes_sec > 0.0
    assert profile.metrics.synthetic_operations_sec is None
    assert profile.metrics.reconstruction_mse >= 0.0

def test_student_checkpoint_reload():
    distiller = RealKnowledgeDistillationService()
    profile = distiller.get_distillation_profile()

    checkpoint_data = torch.load(profile.artifact_path, weights_only=False)
    assert checkpoint_data["model_architecture"] == "StudentPyTorchModel"
    assert "state_dict" in checkpoint_data

    reloaded_student = StudentPyTorchModel()
    reloaded_student.load_state_dict(checkpoint_data["state_dict"])
    reloaded_student.eval()

    test_x = torch.randn(1, 16)
    with torch.no_grad():
        out1 = distiller.student_model(test_x)
        out2 = reloaded_student(test_x)
        assert torch.allclose(out1, out2, atol=1e-5)
