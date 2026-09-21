# Applied Agentic AI — Documentation & Visual Assets Directory

**Course Code:** MR23-1CS0436
**Parent Repository:** [Applied Agentic AI Laboratory Experiments](../README.md)

---

## 📌 Overview

The `docs/` directory serves as the central repository asset hub for:
1. **Architecture & Topology Diagrams:** High-level system architecture charts for complex single and multi-agent workflows.
2. **Workflow & Sequence Charts:** Execution sequence diagrams illustrating data flow, tool calls, and LLM prompt chaining.
3. **Lab Evaluation Documentation:** University submission reports, viva voce review notes, and grading rubrics.
4. **Visual Screenshots:** Verified runtime application screenshots demonstrating web user interfaces, terminal traces, and benchmark metrics.

---

## 📂 Subdirectory Architecture

As experiments are implemented, visual and structural documentation will be organized into the following layout:

```
docs/
│
├── README.md                           # Documentation directory guidelines (this file)
│
├── architecture/                       # System architecture diagrams (.png, .svg, .mmd)
│   ├── exp01-text-to-sql-arch.png
│   ├── exp04-sql-agent-arch.png
│   └── exp05-multi-agent-sdr-arch.png
│
├── workflows/                          # Sequence & prompt pipeline flowcharts
│   ├── exp03-prompt-chain-flow.svg
│   └── exp07-deep-research-loop.svg
│
├── screenshots/                        # Live UI & execution verification screenshots
│   ├── exp01-ui-demo.png
│   └── exp12-capstone-dashboard.png
│
└── lab-notes/                          # Viva voce prep notes & evaluation guidelines
    └── viva-questions-master-guide.md
```

---

## 🎨 Visual Standardization Guidelines

When contributing diagrams or screenshots to `docs/`:

* **Diagram Formats:** Preferred formats are Mermaid (`.mmd`), SVG (`.svg`), or high-resolution PNG (`.png`).
* **Screenshot Resolution:** Ensure screenshots capture key interactive components, agent step-by-step logs, and final query outputs cleanly without displaying API keys or sensitive user data.
* **Naming Convention:** Use lowercase hyphenated filenames prefixed by experiment number (e.g., `exp01-text-to-sql-pipeline.png`).
