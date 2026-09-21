"""
Synthetic Reasoning Benchmark Suite Generator
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
Generates complex benchmark problems for comparative prompting paradigm evaluation.
"""

import json
import os

SYNTHETIC_BENCHMARK_TASKS = [
    {
        "task_id": "TASK-CYBER-01",
        "title": "SOC Ransomware Incident Root-Cause Analysis & Containment",
        "domain": "Cybersecurity",
        "complexity": "High",
        "problem_statement": "An attacker compromised a developer workstation via phishing, escalated privileges using CVE-2023-23397, and initiated lateral movement to the backup server. Determine the root cause, list impacted hosts, and formulate containment steps.",
        "ground_truth_key_factors": ["CVE-2023-23397", "Lateral movement to backup server", "Privilege escalation", "Isolate workstation & reset domain admin credentials"]
    },
    {
        "task_id": "TASK-FIN-02",
        "title": "Multi-Entity Corporate Tax Compliance & Discrepancy Audit",
        "domain": "Financial Audit",
        "complexity": "High",
        "problem_statement": "Subsidiary A reported $4.2M gross revenue with $1.1M cross-border transfer pricing to Subsidiary B. Evaluate whether transfer pricing rules were violated and calculate net tax exposure.",
        "ground_truth_key_factors": ["Transfer pricing compliance", "Cross-border tax exposure", "Documentation audit"]
    },
    {
        "task_id": "TASK-SQL-03",
        "title": "Complex Multi-Join Data Warehousing Query Optimization",
        "domain": "Database Engineering",
        "complexity": "Medium",
        "problem_statement": "A reporting query joining `orders`, `line_items`, and `customers` takes 42 seconds due to full table scans on 10M rows. Propose query rewrite and indexing strategies.",
        "ground_truth_key_factors": ["Composite index on customer_id + order_date", "CTE pre-aggregation", "Covering index"]
    }
]

def generate_benchmark_tasks(output_path: str = None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "benchmark_tasks.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SYNTHETIC_BENCHMARK_TASKS, f, indent=2)

    print(f"[OK] Generated {len(SYNTHETIC_BENCHMARK_TASKS)} benchmark tasks -> {output_path}")

if __name__ == "__main__":
    generate_benchmark_tasks()
