"""
Synthetic Policy & Audit Scenario Dataset Generator
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
Generates structured enterprise security policies and test evaluation scenarios.
"""

import json
import os

SYNTHETIC_POLICIES = [
    {
        "policy_id": "POL-SEC-01",
        "category": "Password & Authentication Security",
        "title": "Corporate Multi-Factor Authentication & Password Standard",
        "version": "2.4.0",
        "rules": [
            {
                "rule_id": "RULE-SEC-01A",
                "name": "MFA Enforcement",
                "description": "Multi-Factor Authentication (MFA) must be enforced for all external remote access, VPN logins, and cloud service admin portals.",
                "required_keywords": ["mfa", "multi-factor", "2fa"],
                "prohibited_actions": ["bypass mfa", "sms-only mfa for root admin"],
                "severity": "CRITICAL",
                "remediation": "Enable TOTP / WebAuthn hardware security keys on all admin and VPN accounts immediately."
            },
            {
                "rule_id": "RULE-SEC-01B",
                "name": "Password Length & Complexity",
                "description": "Passwords must be at least 14 characters long and contain uppercase, lowercase, numbers, and symbols, or use a 16+ character passphrase.",
                "required_keywords": ["14 characters", "passphrase", "complexity"],
                "prohibited_actions": ["hardcoded password", "default password"],
                "severity": "HIGH",
                "remediation": "Enforce automated length and complexity checks via Active Directory / Identity Provider policy."
            }
        ]
    },
    {
        "policy_id": "POL-PII-02",
        "category": "Data Protection & PII Privacy",
        "title": "Customer PII Handling & Storage Standard",
        "version": "3.1.0",
        "rules": [
            {
                "rule_id": "RULE-PII-02A",
                "name": "PII Encryption at Rest and Transit",
                "description": "All personally identifiable information (PII) including emails, phone numbers, and SSNs must be encrypted at rest using AES-256 and in transit using TLS 1.3.",
                "required_keywords": ["aes-256", "tls 1.3", "encryption"],
                "prohibited_actions": ["unencrypted pii", "plaintext pii in logs", "http transmission"],
                "severity": "CRITICAL",
                "remediation": "Configure database column-level AES-256 encryption and disable non-HTTPS endpoints."
            },
            {
                "rule_id": "RULE-PII-02B",
                "name": "PII Log Redaction",
                "description": "Application logs must mask customer email addresses, credit cards, and social security numbers prior to writing to centralized logging platforms.",
                "required_keywords": ["masking", "redaction", "log sanitization"],
                "prohibited_actions": ["print pii to stdout", "unmasked credit card in log"],
                "severity": "HIGH",
                "remediation": "Implement automatic regex log sanitization middleware across all backend services."
            }
        ]
    },
    {
        "policy_id": "POL-AI-03",
        "category": "Generative AI & Model Safety",
        "title": "Enterprise Generative AI & LLM Usage Safeguards",
        "version": "1.2.0",
        "rules": [
            {
                "rule_id": "RULE-AI-03A",
                "name": "Proprietary Source Code Upload Restriction",
                "description": "Employees must not paste unencrypted proprietary core repository code or customer database credentials into public unvetted commercial AI chatbots.",
                "required_keywords": ["public ai", "unvetted chatbot", "proprietary code"],
                "prohibited_actions": ["paste api key into public chat", "upload database credentials"],
                "severity": "CRITICAL",
                "remediation": "Deploy enterprise private AI proxies with zero data retention SLA agreements."
            },
            {
                "rule_id": "RULE-AI-03B",
                "name": "Human-in-the-Loop Verification",
                "description": "All AI-generated code, medical analysis, or financial reports must be reviewed and approved by a qualified human subject matter expert prior to production deployment.",
                "required_keywords": ["human review", "human-in-the-loop", "verification"],
                "prohibited_actions": ["autonomous unverified deployment", "direct AI medical diagnosis"],
                "severity": "HIGH",
                "remediation": "Establish mandatory peer review gates in CI/CD release pipelines."
            }
        ]
    }
]

SYNTHETIC_SCENARIOS = [
    {
        "scenario_id": "SCEN-001",
        "title": "Unencrypted Customer Email Logging Incident",
        "category": "Data Protection & PII Privacy",
        "description": "A developer committed a backend logging middleware that prints raw customer email addresses and unhashed phone numbers directly to public S3 log buckets over HTTP.",
        "target_policy_id": "POL-PII-02",
        "expected_verdict": "NON_COMPLIANT"
    },
    {
        "scenario_id": "SCEN-002",
        "title": "MFA Enforcement on Cloud Admin Console",
        "category": "Password & Authentication Security",
        "title_full": "Compliant AWS Portal MFA Setup",
        "description": "The DevOps team configured WebAuthn hardware security keys and multi-factor authentication for all cloud administrative accounts with zero bypass exceptions.",
        "target_policy_id": "POL-SEC-01",
        "expected_verdict": "COMPLIANT"
    },
    {
        "scenario_id": "SCEN-003",
        "title": "Pasting API Keys into Public Chatbot",
        "category": "Generative AI & Model Safety",
        "description": "An engineer uploaded a production database connection string containing plaintext passwords into a public external web chatbot to ask for SQL optimization help.",
        "target_policy_id": "POL-AI-03",
        "expected_verdict": "NON_COMPLIANT"
    }
]

def generate_policy_data(policies_path: str = None, scenarios_path: str = None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if policies_path is None:
        policies_path = os.path.join(base_dir, "policies.json")
    if scenarios_path is None:
        scenarios_path = os.path.join(base_dir, "scenarios.json")

    os.makedirs(os.path.dirname(policies_path), exist_ok=True)
    with open(policies_path, "w", encoding="utf-8") as f:
        json.dump(SYNTHETIC_POLICIES, f, indent=2)

    with open(scenarios_path, "w", encoding="utf-8") as f:
        json.dump(SYNTHETIC_SCENARIOS, f, indent=2)

    print(f"[OK] Generated {len(SYNTHETIC_POLICIES)} policies and {len(SYNTHETIC_SCENARIOS)} audit scenarios.")

if __name__ == "__main__":
    generate_policy_data()
