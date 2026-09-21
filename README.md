# 🤖 Applied Agentic AI — Laboratory Experiments

**Course Code:** MR23-1CS0436  
**Course Name:** Applied Agentic AI Laboratory  
**Academic Year:** 2025–2026  
**Status:** ✅ 12 / 12 Experiments Completed  
**Automated Verification:** ✅ 164 / 164 Tests Passed (100% Pass Rate)  
**Application Ports:** `8000–8011`  

---

> 📖 **Master Laboratory Guide:**  
> Access the comprehensive technical documentation, execution procedures, visual workflow diagrams, faculty demonstration cheat sheets, and viva voce Q&A preparation in the **[Master Laboratory Guide](AGENTIC_AI_LAB_COMPLETE_GUIDE.md)**.

---

## 📋 Course & Repository Overview

Welcome to the **Applied Agentic AI Laboratory Experiments** repository. This repository serves as a comprehensive, modular suite of **12 laboratory experiments** designed for course **MR23-1CS0436**.

The curriculum advances systematically from foundational prompt engineering and single-turn retrieval pipelines to autonomous ReAct agents, multi-agent coordination systems, reasoning benchmarks, parameter-efficient model adaptation, model optimization, and an end-to-end Capstone decision-support system:

1. **Text-to-SQL Workflow** — Natural-language query translation and SQLite execution.
2. **RAG-Based Question Answering** — Paragraph chunking, TF-IDF / term-frequency retrieval, and grounded response generation.
3. **Prompt Chaining for Summarization** — 6-stage sequential prompt decomposition and workflow memory.
4. **Self-Correcting ReAct SQL Agent** — Autonomous tool execution, schema reflection, and error auto-correction.
5. **Multi-Agent SDR System** — Specialized agents for lead generation, qualification, and draft emailing.
6. **Policy Compliance Checker** — Rule-based governance evaluation and synthetic data validation.
7. **Deep Research Agent Workflow** — Structured research planning, section synthesis, and reflection loops.
8. **Multimodal Visual QA System** — Image metadata parsing, visual search, and multimodal questioning.
9. **Reasoning Model Benchmarking** — Comparative evaluation across Direct, Chain-of-Thought, Tree-of-Thoughts, and ReAct paradigms.
10. **Fine-Tuning for Domain Adaptation** — PyTorch Low-Rank Adaptation (LoRA) neural layer simulation and deterministic evaluation.
11. **Model Optimization Experiment** — INT8/INT4 symmetric quantization and teacher-student knowledge distillation.
12. **Agentic Cybersecurity Capstone** — 7-agent defensive incident decision-support system with 5 safe tools and local RAG.

---

## 🧪 Laboratory Experiments Matrix

| Exp # | Experiment Title | Short Objective | Status | Default Port |
| :---: | :--- | :--- | :---: | :---: |
| **01** | [Text-to-SQL Workflow](experiment-01-text-to-sql) | Build an end-to-end LLM workflow with schema retrieval and query generation. | ✅ Completed | `8000` |
| **02** | [RAG-Based Question Answering System](experiment-02-rag-qa) | Implement paragraph chunking, hybrid term retrieval, and response generation. | ✅ Completed | `8001` |
| **03** | [Prompt Chaining for Summarization](experiment-03-prompt-chaining) | Experiment with 6-stage prompt pipelines, state tracking, and structured decomposition. | ✅ Completed | `8002` |
| **04** | [SQL Agent with Tool Use](experiment-04-sql-agent) | Develop a ReAct-based agent using database tools and schema reflection loops. | ✅ Completed | `8003` |
| **05** | [Multi-Agent SDR System](experiment-05-multi-agent-sdr) | Design specialized agents for lead generation, qualification, and draft emailing. | ✅ Completed | `8004` |
| **06** | [Policy Compliance Agent](experiment-06-policy-compliance) | Build an agent for rule-based policy evaluation and synthetic data validation. | ✅ Completed | `8005` |
| **07** | [Deep Research Agent Workflow](experiment-07-deep-research) | Implement planning and reflection loops for structured technical report synthesis. | ✅ Completed | `8006` |
| **08** | [Image Retrieval / Visual QA System](experiment-08-visual-qa) | Develop a multimodal pipeline for visual questioning and image metadata search. | ✅ Completed | `8007` |
| **09** | [Reasoning Model Benchmarking](experiment-09-reasoning-benchmark) | Compare outputs across Direct, CoT, ToT, and ReAct reasoning paradigms. | ✅ Completed | `8008` |
| **10** | [Fine-Tuning for Domain Adaptation](experiment-10-fine-tuning) | Implement PyTorch LoRA neural layer adaptation and deterministic evaluation. | ✅ Completed | `8009` |
| **11** | [Model Optimization Experiment](experiment-11-model-optimization) | Apply INT8/INT4 symmetric quantization and teacher-student distillation. | ✅ Completed | `8010` |
| **12** | [Agentic Cybersecurity Assistant (Capstone)](experiment-12-capstone) | Deploy a 7-agent defensive incident decision assistant with 5 tools and local RAG. | ✅ Completed | `8011` |

---

## 🧠 What This Repository Demonstrates

Across the 12 experiments, this repository demonstrates key core paradigms in Agentic AI engineering:

* **Natural-Language-to-Structured-Action:** Mapping conversational queries to schema-validated SQL statements.
* **Retrieval-Augmented Generation (RAG):** Document chunking, TF-IDF / term-frequency relevance ranking, and evidence grounding.
* **Prompt Chaining & State Management:** Multi-stage prompt execution pipelines preserving contextual state across steps.
* **Tool-Using ReAct Architecture:** Autonomous Reasoning + Acting execution loops with schema reflection and error recovery.
* **Multi-Agent Collaboration:** Supervisor-directed and role-specialized agent pipelines with explicit handoff protocols.
* **Governance & Policy Auditing:** Deterministic policy compliance checking and evidence-supported audit logging.
* **Planning & Bounded Reflection:** Dynamic task plan generation and iterative critique/review cycles.
* **Multimodal Visual Processing:** Combining visual metadata, image feature extraction, and text synthesis.
* **Reasoning Paradigm Benchmarking:** Quantitative evaluation comparing Direct, CoT, ToT, and ReAct performance.
* **Parameter-Efficient Model Adaptation:** Low-Rank Adaptation (LoRA) trainable parameter isolation and rank mechanics.
* **Model Optimization & Compression:** INT8/INT4 symmetric quantization transformations and KL-divergence knowledge distillation.
* **Defensive Cybersecurity Decision Support:** End-to-end incident triage, IOC extraction, MITRE ATT&CK mapping, and compliance auditing.
* **Production-Grade Application Engineering:** FastAPI REST web services, responsive dark-mode UIs, structured logging, and automated PyTest suites.

---

## 🛠️ Technology Stack

### Core Runtimes & Frameworks
* **Language & Runtime:** Python 3.10+
* **REST Web Services:** FastAPI, Uvicorn (ASGI Application Server)
* **Data Validation & Settings:** Pydantic V2, Pydantic-Settings

### Machine Learning & Data Engines
* **Tensor Mechanics & Optimization:** PyTorch (`torch`) — autograd tensor transformations, LoRA layer simulation, quantization scaling, and distillation loss computation
* **Databases & ORM:** SQLite, SQLAlchemy (relational database storage, schema reflection, read-only queries)
* **Multimodal Processing:** Pillow (`PIL`) — image loading, format validation, and metadata extraction

### Frontend & Dashboards
* **Web Interfaces:** HTML5, Vanilla CSS, JavaScript (ES6+ Async/Fetch) — single-page control dashboards and command centers for all 12 experiments

### Testing & Verification
* **Automated Testing:** PyTest, HTTPX, Requests, Starlette TestClient (164 passing tests across repository)

---

## 📂 Repository Structure

```text
Agentic AI Experiments/
│
├── README.md                           # Main repository documentation & status matrix
├── AGENTIC_AI_LAB_COMPLETE_GUIDE.md    # Complete 26-chapter Master Laboratory Guide
├── .gitignore                          # Excludes secrets, venvs, cache, and DBs
├── LICENSE                             # MIT License
│
├── experiment-01-text-to-sql/          # Exp 1: Text-to-SQL Workflow (✅ Completed)
│   └── README.md
├── experiment-02-rag-qa/               # Exp 2: RAG-Based QA System (✅ Completed)
│   └── README.md
├── experiment-03-prompt-chaining/      # Exp 3: Prompt Chaining Summarization (✅ Completed)
│   └── README.md
├── experiment-04-sql-agent/            # Exp 4: ReAct SQL Agent with Tool Use (✅ Completed)
│   └── README.md
├── experiment-05-multi-agent-sdr/      # Exp 5: Multi-Agent SDR System (✅ Completed)
│   └── README.md
├── experiment-06-policy-compliance/   # Exp 6: Policy Compliance Agent (✅ Completed)
│   └── README.md
├── experiment-07-deep-research/        # Exp 7: Deep Research Agent Workflow (✅ Completed)
│   └── README.md
├── experiment-08-visual-qa/            # Exp 8: Visual QA & Image Retrieval (✅ Completed)
│   └── README.md
├── experiment-09-reasoning-benchmark/  # Exp 9: Reasoning Model Benchmarking (✅ Completed)
│   └── README.md
├── experiment-10-fine-tuning/          # Exp 10: Fine-Tuning Domain Adaptation (✅ Completed)
│   └── README.md
├── experiment-11-model-optimization/  # Exp 11: Model Quantization & Distillation (✅ Completed)
│   └── README.md
├── experiment-12-capstone/             # Exp 12: Agentic Cybersecurity Capstone (✅ Completed)
│   └── README.md
│
└── docs/                               # System diagrams & supplementary resources
    └── README.md
```

---

## ⚙️ Quick Execution Reference

For detailed step-by-step instructions, execution logs, and viva voce preparation, view the **[Master Laboratory Guide](AGENTIC_AI_LAB_COMPLETE_GUIDE.md)**.

### Launch Any Experiment Web Application

```powershell
# Experiment 01 — Text-to-SQL Workflow (Port 8000)
cd experiment-01-text-to-sql; python -m app.main

# Experiment 02 — RAG-Based Question Answering System (Port 8001)
cd experiment-02-rag-qa; python -m app.main

# Experiment 03 — Prompt Chaining for Summarization (Port 8002)
cd experiment-03-prompt-chaining; python -m app.main

# Experiment 04 — Self-Correcting ReAct SQL Agent (Port 8003)
cd experiment-04-sql-agent; python -m app.main

# Experiment 05 — Multi-Agent SDR System (Port 8004)
cd experiment-05-multi-agent-sdr; python -m app.main

# Experiment 06 — Policy Compliance Checker (Port 8005)
cd experiment-06-policy-compliance; python -m app.main

# Experiment 07 — Deep Research Agent Workflow (Port 8006)
cd experiment-07-deep-research; python -m app.main

# Experiment 08 — Multimodal Visual QA System (Port 8007)
cd experiment-08-visual-qa; python -m app.main

# Experiment 09 — Reasoning Model Benchmarking (Port 8008)
cd experiment-09-reasoning-benchmark; python -m app.main

# Experiment 10 — Fine-Tuning for Domain Adaptation (Port 8009)
cd experiment-10-fine-tuning; python -m app.main

# Experiment 11 — Model Optimization Experiment (Port 8010)
cd experiment-11-model-optimization; python -m app.main

# Experiment 12 — Agentic Cybersecurity Capstone (Port 8011)
cd experiment-12-capstone; python -m app.main
```

### Run Automated Tests

To run the automated test suite for any specific experiment:

```powershell
cd experiment-XX-name
python -m pytest tests -v
```

---

## ✅ Final Verification Status

* **Completed Modules:** **12 / 12 Experiments** fully implemented, tested, and verified.
* **Test Suite Pass Rate:** **164 / 164 PyTest assertions PASSED** across the repository.
* **Server Port Allocation:** Ports `8000–8011` strictly assigned without collisions.
* **Experiment 10 Canonical Workflow:** PyTorch LoRA simulation verified (`CyberSecurity-Base-Model-v1`, base seed 42, LoRA seed 100, 5 epochs, lr 0.05, rank 8, alpha 16) producing deterministic base accuracy $20.0\%$, trained accuracy $40.0\%$ ($+20.0$ percentage points gain / $+100.0\%$ relative improvement).
* **Experiment 11 Model Optimization:** INT8/INT4 symmetric quantization scaling and teacher-student knowledge distillation engines fully operational.
* **Experiment 12 Agentic Capstone:** 7-agent multi-agent pipeline (`SupervisorAgent`, `RetrievalAgent`, `ToolAgent`, `SecurityAnalysisAgent`, `ComplianceVerificationAgent`, `ReflectionCriticAgent`, `SynthesisAgent`) and 5 safe cybersecurity tools (`KnowledgeSearchTool`, `IOCParserTool`, `RiskCalculatorTool`, `MITRELookupTool`, `IncidentTimelineBuilderTool`) verified on Port `8011`.

---

## 👨‍💻 Author & Developer

**Ardha Nikhitha**  
B.Tech — Computer Science & Engineering  

**GitHub:** [nikhithaardha-cell](https://github.com/nikhithaardha-cell)  

> This repository was designed, implemented, tested, documented, and maintained by **G. Vaishnav Kumar** as part of the **Applied Agentic AI Laboratory (MR23-1CS0436)** for the **2025–2026 academic year**.

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE) — created for educational, laboratory, research, and portfolio purposes under course **MR23-1CS0436**.
