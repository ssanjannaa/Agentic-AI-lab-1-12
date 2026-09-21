"""
Real PyTorch Model & Autograd LoRA Unit Tests
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

import os
import tempfile
import torch
from app.services.model_engine import CyberSecurityPyTorchLoRAModel

def test_pytorch_nn_module_subclass():
    model = CyberSecurityPyTorchLoRAModel(in_dim=16, out_dim=4, lora_rank=8, lora_alpha=16)
    assert isinstance(model, torch.nn.Module)

def test_trainable_and_frozen_parameter_counts():
    model = CyberSecurityPyTorchLoRAModel(in_dim=16, out_dim=4, lora_rank=8, lora_alpha=16)
    assert model.get_frozen_parameter_count() == 68
    assert model.get_trainable_parameter_count() == 160

def test_pytorch_autograd_training_parameter_change():
    model = CyberSecurityPyTorchLoRAModel(in_dim=16, out_dim=4, lora_rank=8, lora_alpha=16)
    snapshot_before = model.get_parameter_snapshot()

    x = torch.tensor([[0.5] * 16], dtype=torch.float32)
    y = torch.tensor([0], dtype=torch.long)

    loss1 = model.train_step(x, y)
    loss2 = model.train_step(x, y)

    trainable_diff, frozen_diff = model.compute_parameter_change_norm(snapshot_before)
    assert frozen_diff == 0.0, "Frozen base parameters must NOT change!"
    assert trainable_diff > 0.0, "Trainable LoRA parameters must numerically change after training steps!"

def test_checkpoint_save_and_reload():
    model = CyberSecurityPyTorchLoRAModel(in_dim=16, out_dim=4, lora_rank=8, lora_alpha=16)
    x = torch.tensor([[0.2] * 16], dtype=torch.float32)
    y = torch.tensor([1], dtype=torch.long)
    model.train_step(x, y)

    with tempfile.TemporaryDirectory() as tmpdir:
        ckpt_path = os.path.join(tmpdir, "lora_adapter.pt")
        model.save_checkpoint(ckpt_path)
        assert os.path.exists(ckpt_path)

        new_model = CyberSecurityPyTorchLoRAModel(in_dim=16, out_dim=4, lora_rank=8, lora_alpha=16)
        new_model.load_checkpoint(ckpt_path)

        assert torch.equal(new_model.lora_A, model.lora_A)
        assert torch.equal(new_model.lora_B, model.lora_B)
        assert torch.equal(new_model.base_layer.weight, model.base_layer.weight)
