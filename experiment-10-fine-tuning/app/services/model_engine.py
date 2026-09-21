"""
PyTorch LoRA Parameter Fine-Tuning & Autograd Model Engine
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)

Implements a genuine PyTorch nn.Module with frozen base parameters, trainable LoRA adapter parameters,
autograd backpropagation, PyTorch optimizer updates, checkpoint serialization, and parameter delta verification.
"""

import os
import math
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict, Any, Tuple

class CyberSecurityPyTorchLoRAModel(nn.Module):
    def __init__(self, in_dim: int = 16, out_dim: int = 4, lora_rank: int = 8, lora_alpha: float = 16.0):
        super().__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.lora_rank = lora_rank
        self.lora_alpha = lora_alpha
        self.scaling = lora_alpha / lora_rank

        torch.manual_seed(42)

        # 1. Base Model Parameters (FROZEN - requires_grad = False)
        self.base_layer = nn.Linear(in_dim, out_dim)
        self.base_layer.weight.requires_grad = False
        self.base_layer.bias.requires_grad = False

        # 2. LoRA Adapter Parameters (TRAINABLE - requires_grad = True)
        torch.manual_seed(100)
        self.lora_A = nn.Parameter(torch.randn(lora_rank, in_dim) * 0.1, requires_grad=True)
        self.lora_B = nn.Parameter(torch.zeros(out_dim, lora_rank), requires_grad=True)

        # 3. PyTorch Optimizer
        self.optimizer = optim.Adam([self.lora_A, self.lora_B], lr=0.01)
        self.criterion = nn.CrossEntropyLoss()

    def get_frozen_parameter_count(self) -> int:
        return self.base_layer.weight.numel() + self.base_layer.bias.numel()

    def get_trainable_parameter_count(self) -> int:
        return self.lora_A.numel() + self.lora_B.numel()

    def forward(self, x: torch.Tensor, enable_lora: bool = True) -> torch.Tensor:
        # x shape: (batch_size, in_dim) or (in_dim,)
        if x.dim() == 1:
            x = x.unsqueeze(0)

        base_out = self.base_layer(x)
        if not enable_lora:
            return base_out

        # LoRA forward pass: (x @ A^T) @ B^T * scaling
        h = torch.matmul(x, self.lora_A.T) # (batch_size, lora_rank)
        lora_out = torch.matmul(h, self.lora_B.T) * self.scaling # (batch_size, out_dim)

        return base_out + lora_out

    def train_step(self, x: torch.Tensor, target: torch.Tensor) -> float:
        self.train()
        self.optimizer.zero_grad()

        outputs = self.forward(x, enable_lora=True)
        loss = self.criterion(outputs, target)

        # Genuine PyTorch Autograd Backpropagation
        loss.backward()

        # Verify frozen parameters received NO gradients
        assert self.base_layer.weight.grad is None, "Frozen base weights received unexpected gradient!"
        assert self.base_layer.bias.grad is None, "Frozen base bias received unexpected gradient!"

        # PyTorch Optimizer Step
        self.optimizer.step()

        return float(loss.item())

    def get_parameter_snapshot(self) -> Dict[str, torch.Tensor]:
        return {
            "base_weight": self.base_layer.weight.clone().detach(),
            "base_bias": self.base_layer.bias.clone().detach(),
            "lora_A": self.lora_A.clone().detach(),
            "lora_B": self.lora_B.clone().detach()
        }

    def compute_parameter_change_norm(self, snapshot_before: Dict[str, torch.Tensor]) -> Tuple[float, float]:
        with torch.no_grad():
            # Trainable LoRA parameter change norm
            trainable_diff = (
                torch.sum((self.lora_A - snapshot_before["lora_A"]) ** 2) +
                torch.sum((self.lora_B - snapshot_before["lora_B"]) ** 2)
            ).sqrt().item()

            # Frozen base parameter change norm (Must be 0.0)
            frozen_diff = (
                torch.sum((self.base_layer.weight - snapshot_before["base_weight"]) ** 2) +
                torch.sum((self.base_layer.bias - snapshot_before["base_bias"]) ** 2)
            ).sqrt().item()

        return float(trainable_diff), float(frozen_diff)

    def save_checkpoint(self, checkpoint_path: str):
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        checkpoint_data = {
            "model_architecture": "CyberSecurityPyTorchLoRAModel",
            "in_dim": self.in_dim,
            "out_dim": self.out_dim,
            "lora_rank": self.lora_rank,
            "lora_alpha": self.lora_alpha,
            "state_dict": {
                "base_weight": self.base_layer.weight.data,
                "base_bias": self.base_layer.bias.data,
                "lora_A": self.lora_A.data,
                "lora_B": self.lora_B.data
            }
        }
        torch.save(checkpoint_data, checkpoint_path)

    def load_checkpoint(self, checkpoint_path: str):
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint file '{checkpoint_path}' not found.")

        checkpoint_data = torch.load(checkpoint_path, weights_only=False)
        state_dict = checkpoint_data["state_dict"]

        with torch.no_grad():
            self.lora_A.copy_(state_dict["lora_A"])
            self.lora_B.copy_(state_dict["lora_B"])
