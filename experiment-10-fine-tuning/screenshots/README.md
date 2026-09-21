# Experiment 10 — Screenshots & Visual Artifacts Directory

**Course Code:** MR23-1CS0436  
**Experiment Name:** Fine-Tuning for Domain Adaptation  

---

## 📌 Overview

This directory stores verified visual evidence and runtime application screenshots demonstrating the **Fine-Tuning for Domain Adaptation** web application running on port `8009`.

---

## 📷 Verified Screenshots & Cryptographic Hashes

| View | Filename | SHA-256 Hash | Byte Size |
| :--- | :--- | :--- | :--- |
| **01. Initial Home Interface** | `01-home-interface.png` | `C7DF75DDD5B60B0B49130962AACD44391AE2C393C978BB7C4144A5BF831984BD` | 297,268 B |
| **02. PyTorch Training Loss Curves** | `02-training-loss-curves.png` | `7D6FF55CBB21F852E7FD77ABE21B5482C44467F9D7C8F5786D1DA34020ED51BE` | 262,680 B |
| **03. Base vs Fine-Tuned Evaluation** | `03-base-vs-finetuned-eval.png` | `97A056A7AF0BCD6F26898F320AC4578104B845768FAA0A67CC4B14E34E8E67EC` | 303,325 B |
| **04. Accuracy Improvement Gauge** | `04-accuracy-improvement-gauge.png` | `F9250C2D6E8C6C700E80F9C0325F40DD921D26F7A22DB936A08885533ED47DC7` | 275,762 B |

### Verified View Contents:
1. **`01-home-interface.png`**: Initial Web UI studio setup showing canonical LoRA hyperparameter controls (Rank $r=8$, $\alpha=16$, Epochs=5, LR=0.05), dataset statistics, and empty training workbench.
2. **`02-training-loss-curves.png`**: Training job execution summary (`Trainable Params: 160`, `Frozen Base Params: 68`, `Delta Trainable: +1.733159 > 0.0`, `Delta Frozen: 0.000000`) and epoch loss trajectory table across 5 epochs.
3. **`03-base-vs-finetuned-eval.png`**: Base Model (LoRA Disabled, 20.0% accuracy) vs. Fine-Tuned Model (LoRA Adapted, 40.0% accuracy) side-by-side comparison cards displaying +20.0 percentage points gain (+100.0% relative).
4. **`04-accuracy-improvement-gauge.png`**: Scrolled detailed benchmark evaluation section highlighting the green Fine-Tuned Model accuracy badge (40.0%), mitigation instructions output, and bottom metric banner (`Evaluated Correct: 4 / 10 samples (+20 percentage points gain | +100% relative)`).
