# Experiment 10 — Fine-Tuning for Domain Adaptation

**Course Code:** MR23-1CS0436  
**Course Name:** Applied Agentic AI  
**Laboratory:** Applied Agentic AI Laboratory  
**Status:** ✅ Completed & Verified  
**Directory:** `experiment-10-fine-tuning`  
**Port:** `8009`  

---

## 🎯 A. Experiment Title
**Fine-Tuning for Domain Adaptation System**

---

## 📚 B. Course Details
- **Course Code:** MR23-1CS0436
- **Course Name:** Applied Agentic AI
- **Laboratory:** Applied Agentic AI Laboratory
- **Module Type:** Real PyTorch PEFT / LoRA Parameter Training & Base vs. Fine-Tuned Benchmark

---

## 📌 C. Status
✅ **Completed & Verified** (13 Automated PyTest Tests Passed, Runtime UI Verified on Port 8009)

---

## 🎯 D. Aim
To design, build, and evaluate a real PyTorch PEFT/LoRA Fine-Tuning system for domain adaptation, executing autograd backpropagation over trainable adapter tensors, tracking epoch loss decay and perplexity, proving numerical parameter value change ($\Delta \theta > 0$), saving trained checkpoint artifacts (`checkpoints/lora_adapter.pt`), and benchmarking Base Model (LoRA disabled) vs. Fine-Tuned Model (LoRA adapter enabled) outputs programmatically.

> **Educational Model Identity & Scope Disclosure:** This experiment constructs a lightweight educational PyTorch `nn.Module` (`CyberSecurityPyTorchLoRAModel`) to demonstrate genuine autograd parameter updates, frozen base weights, and state dict checkpoint reloading without needing an impractically large external LLM download.

---

## 🎯 E. Learning Objectives
1. **Real PyTorch PEFT / LoRA Parameter Fine-Tuning:** Implement trainable adapter matrices ($A \in \mathbb{R}^{r \times d}, B \in \mathbb{R}^{d \times r}$) over frozen base model weights ($W_0$).
2. **PyTorch Autograd Backpropagation:** Execute forward pass, loss calculation, `loss.backward()` gradient computation, and `optimizer.step()` Adam parameter updates.
3. **Parameter Change Verification:** Prove numerical weight updates by calculating $\Delta \theta = \| \theta_{\text{final}} - \theta_{\text{initial}} \| > 0.0$ while asserting frozen base parameters remain unchanged ($\Delta \theta_{\text{frozen}} == 0.0$).
4. **Checkpoint Serialization & Reloading:** Save trained adapter weights to `checkpoints/lora_adapter.pt`, reload state dicts into model instances, and programmatically evaluate domain adaptation performance over 10 evaluation samples.

---

## 📜 F. Problem Statement
General-purpose LLMs struggle with specialized enterprise domains (such as cybersecurity vulnerability remediation, post-quantum cryptography, and regulatory PII compliance), producing generic responses or domain hallucinations. Full parameter fine-tuning is computationally expensive. **Parameter-Efficient Fine-Tuning (PEFT / LoRA)** freezes base model weights and trains lightweight rank-adapter matrices, drastically reducing trainable parameter counts while adapting the model to domain tasks.

---

## 💡 G. Real Training System Architecture & Parameter Division
- **Base Model Identifier:** `CyberSecurity-Base-Model-v1` (Educational PyTorch `nn.Module`)
- **Base Model Seed:** `42` (`torch.manual_seed(42)` for base layer weights)
- **LoRA Adapter Seed:** `100` (`torch.manual_seed(100)` for adapter matrices $A, B$)
- **Frozen Base Parameters ($W_0, b_0$):** 68 frozen parameters (`requires_grad = False`).
- **Trainable LoRA Adapter Parameters ($A, B$):** 160 trainable parameters for rank $r=8$ (`requires_grad = True`).
- **Canonical Hyperparameter Configuration:** `num_epochs = 5, learning_rate = 0.05, lora_rank = 8, lora_alpha = 16`.
- **Dataset Partitioning:** 4 training instruction samples, 2 validation samples, 10 evaluation samples (`data/eval_dataset.jsonl`).
- **Parameter Change Proof:** Initial adapter weights $B = \mathbf{0}$. After training epochs, $\Delta \theta_{\text{trainable}} = \| B_{\text{final}} - B_{\text{initial}} \| = +1.733159 > 0.0$ while $\Delta \theta_{\text{frozen}} == 0.000000$.
- **Canonical Benchmark Metric:** Base Accuracy = 20.0% (2/10), Trained Checkpoint Accuracy = 40.0% (4/10), Difference = +20.0 percentage points gain (+100.0% relative improvement).
- **Checkpoint Artifact:** Serialized to `checkpoints/lora_adapter.pt`.

---

## 🏗️ H. System Architecture

```mermaid
graph TD
    A["User Request / Hyperparameters (r=8, alpha=16, epochs=5, lr=0.05)"] --> B["RealLoRATrainer (app/services/trainer.py)"]
    B --> C["CyberSecurityPyTorchLoRAModel (app/services/model_engine.py)"]
    C --> D["Frozen Base Layer (68 Params, requires_grad=False)"]
    C --> E["Trainable LoRA Adapters (160 Params, requires_grad=True)"]
    B --> F["PyTorch Autograd Training Loop (loss.backward(), optimizer.step())"]
    F --> G["Parameter Change Verification (delta_trainable > 0, delta_frozen == 0)"]
    G --> H["PyTorch Checkpoint Serialization (checkpoints/lora_adapter.pt)"]
    H --> I["ModelEvaluatorService (app/services/evaluator.py)"]
    I --> J["Programmatic Evaluation (10 eval samples, Base vs Fine-Tuned Accuracy)"]
```

---

## 🧪 I. Test Suite & Verification Results
```powershell
python -m pytest experiment-10-fine-tuning/tests -v
# Output: 13 passed in 6.98s
```

### Verified Test Assertions:
1. `test_pytorch_nn_module_subclass`: Verifies model subclasses `torch.nn.Module`.
2. `test_trainable_and_frozen_parameter_counts`: Verifies 68 frozen vs 160 trainable parameters.
3. `test_pytorch_autograd_training_parameter_change`: Asserts `frozen_diff == 0.0` and `trainable_diff > 0.0`.
4. `test_checkpoint_save_and_reload`: Verifies PyTorch `torch.save()` and `torch.load()` state dict equality.
5. `test_evaluate_models_comparison`: Verifies programmatic evaluation over 10 evaluation dataset samples and verifies mathematical invariants ($0 \le \text{accuracy} \le 100$, $\text{diff} = \text{trained} - \text{base}$).
6. `test_canonical_reproducible_workflow_consistency`: Verifies exact canonical checkpoint evaluation metrics (Base: 20.0%, Trained: 40.0%, Diff: +20.0 percentage points gain, Rel: +100.0%).

---

## 📷 J. UI Screenshots & Hashes

| View | Screenshot Filename | SHA-256 Hash | Byte Size |
| :--- | :--- | :--- | :--- |
| **01. Initial Studio Interface** | `screenshots/01-home-interface.png` | `C7DF75DDD5B60B0B49130962AACD44391AE2C393C978BB7C4144A5BF831984BD` | 297,268 B |
| **02. PyTorch Training Loss Curves** | `screenshots/02-training-loss-curves.png` | `7D6FF55CBB21F852E7FD77ABE21B5482C44467F9D7C8F5786D1DA34020ED51BE` | 262,680 B |
| **03. Base vs Fine-Tuned Evaluation** | `screenshots/03-base-vs-finetuned-eval.png` | `97A056A7AF0BCD6F26898F320AC4578104B845768FAA0A67CC4B14E34E8E67EC` | 303,325 B |
| **04. Accuracy Improvement Gauge** | `screenshots/04-accuracy-improvement-gauge.png` | `F9250C2D6E8C6C700E80F9C0325F40DD921D26F7A22DB936A08885533ED47DC7` | 275,762 B |

---

## ❓ K. Viva Voce Q&A Preparation

1. **Q: What is the primary objective of Experiment 10?**
   *A:* To build a real PyTorch PEFT/LoRA training engine that freezes base parameters, trains adapter weights using autograd backpropagation, serializes checkpoints, and programmatically evaluates domain adaptation gains.
2. **Q: How does PEFT / LoRA differ from full parameter fine-tuning?**
   *A:* Full fine-tuning updates all model parameters ($W_0$). LoRA freezes $W_0$ (`requires_grad = False`) and injects low-rank trainable matrices $A$ and $B$ (`requires_grad = True`), reducing trainable parameters by over 90%.
3. **Q: How is parameter update verified in this experiment?**
   *A:* By computing $\Delta \theta = \| \theta_{\text{final}} - \theta_{\text{initial}} \|$. The system asserts $\Delta \theta_{\text{trainable}} > 0.0$ and $\Delta \theta_{\text{frozen}} == 0.0$.
4. **Q: How are trained checkpoint artifacts serialized and reloaded?**
   *A:* Via `torch.save(checkpoint_data, path)` and `torch.load(path)`. The evaluator reloads state dicts to instantiate trained models for benchmark evaluation.
5. **Q: What default port is reserved for Experiment 10?**
   *A:* Port `8009`.
6. **Q: How are evaluation accuracy metrics computed?**
   *A:* Accuracy is programmatically derived from predictions over 10 dataset samples in `eval_dataset.jsonl` ($\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Samples}} \times 100$).
7. **Q: What parameters are frozen vs trainable in this model setup?**
   *A:* Base linear weights ($W_0 \in \mathbb{R}^{4 \times 16}, b_0 \in \mathbb{R}^{4}$, 68 params) are frozen. LoRA adapter matrices ($A \in \mathbb{R}^{8 \times 16}, B \in \mathbb{R}^{4 \times 8}$, 160 params) are trainable.
8. **Q: What loss function and optimizer are used?**
   *A:* PyTorch `nn.CrossEntropyLoss` and `torch.optim.Adam` optimizer.
9. **Q: What datasets are used for training and evaluation?**
   *A:* `data/train_dataset.jsonl` (4 samples), `data/val_dataset.jsonl` (2 samples), and `data/eval_dataset.jsonl` (10 samples).
10. **Q: How many automated tests cover Experiment 10?**
    *A:* 13 automated PyTest unit and integration tests.
