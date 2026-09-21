"""
Synthetic Fine-Tuning Domain Dataset Generator
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
Generates instruction-tuning datasets for cybersecurity domain adaptation benchmarking.
"""

import json
import os

TRAIN_SAMPLES = [
    {
        "instruction": "Explain how to mitigate CVE-2023-23397 Outlook vulnerability in an enterprise environment.",
        "input": "System environment: Windows Server 2019, Microsoft 365 Hybrid.",
        "output": "To mitigate CVE-2023-23397: 1. Apply Microsoft KB5023151 security update across all Exchange servers. 2. Block outbound port TCP 445 at edge firewalls to prevent NTLM hash leakage. 3. Audit Active Directory for unusual NTLM authentication attempts using PowerShell script CVE-2023-23397.ps1.",
        "domain_label": 0
    },
    {
        "instruction": "Formulate a policy log masking rule for customer social security numbers (SSN).",
        "input": "Format: 9-digit US SSN (XXX-XX-XXXX).",
        "output": "Enforce Log Masking Rule RULE-PII-02B: Apply regex string replacement r'\\b\\d{3}-\\d{2}-\\d{4}\\b' -> '[SSN-REDACTED]' prior to stdout streaming.",
        "domain_label": 1
    },
    {
        "instruction": "What is the recommended NIST Post-Quantum Cryptography key exchange algorithm?",
        "input": "Target SLA: TLS 1.3 hybrid key encapsulation.",
        "output": "The NIST standardized post-quantum key encapsulation algorithm is CRYSTALS-Kyber (FIPS 203), recommended in hybrid mode paired with ECDH P-256 for backward compatibility.",
        "domain_label": 2
    },
    {
        "instruction": "Formulate incident response steps for ransomware detection on core domain controllers.",
        "input": "Alert: Active SMB volume encryption detected.",
        "output": "1. Isolate domain controller network interface. 2. Disable compromised Service Admin accounts. 3. Restore Active Directory database from offline immutable backup.",
        "domain_label": 3
    }
]

VAL_SAMPLES = [
    {
        "instruction": "How do you detect unauthorized lateral movement via SMB in SOC logs?",
        "input": "Log source: Windows Event ID 5140 (Network Share Access).",
        "output": "Filter Event ID 5140 for access to administrative shares (C$, ADMIN$) originating from non-administrative IP subnets within short time windows.",
        "domain_label": 0
    },
    {
        "instruction": "What encryption standard is required for stored customer PII under GDPR?",
        "input": "Target data: Database columns containing phone numbers and emails.",
        "output": "Enforce AES-256 GCM authenticated encryption at rest and TLS 1.3 in transit.",
        "domain_label": 1
    }
]

EVAL_SAMPLES = [
    {
        "instruction": "Explain how to mitigate CVE-2023-23397 Outlook vulnerability in an enterprise environment.",
        "input": "System environment: Windows Server 2019, Microsoft 365 Hybrid.",
        "expected_output": "Apply KB5023151 update, block outbound TCP 445, and audit NTLM hashes.",
        "domain_label": 0
    },
    {
        "instruction": "Formulate a policy log masking rule for customer social security numbers (SSN).",
        "input": "Format: 9-digit US SSN (XXX-XX-XXXX).",
        "expected_output": "Apply regex r'\\b\\d{3}-\\d{2}-\\d{4}\\b' replacement with [SSN-REDACTED].",
        "domain_label": 1
    },
    {
        "instruction": "What is the recommended NIST Post-Quantum Cryptography key exchange algorithm?",
        "input": "Target SLA: TLS 1.3 hybrid key encapsulation.",
        "expected_output": "CRYSTALS-Kyber (FIPS 203) in hybrid mode with ECDH P-256.",
        "domain_label": 2
    },
    {
        "instruction": "How do you detect unauthorized lateral movement via SMB in SOC logs?",
        "input": "Log source: Windows Event ID 5140 (Network Share Access).",
        "expected_output": "Filter Event ID 5140 for access to administrative shares (C$, ADMIN$).",
        "domain_label": 0
    }
]

def generate_datasets(train_path: str = None, val_path: str = None, eval_path: str = None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if train_path is None:
        train_path = os.path.join(base_dir, "train_dataset.jsonl")
    if val_path is None:
        val_path = os.path.join(base_dir, "val_dataset.jsonl")
    if eval_path is None:
        eval_path = os.path.join(base_dir, "eval_dataset.jsonl")

    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    with open(train_path, "w", encoding="utf-8") as f:
        for item in TRAIN_SAMPLES:
            f.write(json.dumps(item) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for item in VAL_SAMPLES:
            f.write(json.dumps(item) + "\n")

    with open(eval_path, "w", encoding="utf-8") as f:
        for item in EVAL_SAMPLES:
            f.write(json.dumps(item) + "\n")

    print(f"[OK] Generated {len(TRAIN_SAMPLES)} train, {len(VAL_SAMPLES)} val & {len(EVAL_SAMPLES)} eval instruction samples.")

if __name__ == "__main__":
    generate_datasets()
