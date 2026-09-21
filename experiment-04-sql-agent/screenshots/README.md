# Experiment 04 — Screenshots & Visual Artifacts Directory

**Course Code:** MR23-1CS0436
**Experiment Name:** Autonomous ReAct SQL Agent with Tool Use

---

## 📌 Overview

This directory stores verified visual evidence and runtime application screenshots demonstrating the **Autonomous ReAct SQL Agent** web application.

---

## 📷 Verified Verification Screenshots

The following 6 high-resolution screenshot artifacts document the application's visual flow, safe execution trace timeline, tool invocation metrics, grounded database answers, and database schema inspector:

1. **`01-home-interface.png`**
   - Captures the initial Chatbot UI with the header title, loaded status badges (`company.db`, Port `8003`), sample question chips, and empty workbench placeholder.
2. **`02-agent-execution-trace.png`**
   - Captures the active timeline of the **Safe Agent Execution Trace** showing sequential DECIDE → ACT → OBSERVE → VALIDATE steps with step numbers, tool names, decision summaries, and observations.
3. **`03-tool-invocations.png`**
   - Captures the **Agent Tool Usage Metrics** panel displaying counts for `list_tables`, `get_schema`, `check_query_syntax`, `execute_sql`, retries, and total invocations.
4. **`04-final-database-answer.png`**
   - Captures the **Grounded Database Answer** card, executed SQL query block, row count, and execution result data table.
5. **`05-error-correction-retry.png`**
   - Captures the agent trace showing error reflection and retry auto-correction behavior (Attempt 1 trial warning → reflection note → Attempt 2 refined execution).
6. **`06-database-explorer-safety.png`**
   - Captures the interactive **Database Explorer** tabbed schema viewer displaying columns, data types, primary keys, and foreign key relations for `company.db`.

---

## 🎨 Asset Naming Standard
- Format: Lowercase hyphenated string (e.g., `01-home-interface.png`).
- Format type: `.png`.
