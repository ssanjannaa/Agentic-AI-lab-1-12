"""
Query Normalization Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Normalizes user queries by unrolling common cybersecurity acronyms and aliases
to improve semantic embedding and lexical retrieval quality.
"""

import re
from typing import Dict

CYBERSECURITY_ALIASES: Dict[str, str] = {
    "sqli": "sql injection",
    "mfa": "multi-factor authentication",
    "2fa": "two-factor authentication",
    "ids": "intrusion detection system",
    "ips": "intrusion prevention system",
    "siem": "security information and event management",
    "xss": "cross-site scripting",
    "csrf": "cross-site request forgery",
    "waf": "web application firewall",
    "soc": "security operations center",
    "edr": "endpoint detection and response",
    "csp": "content security policy"
}

def normalize_query(query: str) -> str:
    """
    Normalizes input query for retrieval:
    1. Lowercases query.
    2. Identifies cybersecurity acronyms/aliases.
    3. Appends expanded terms to preserve both acronym and full domain phrase.
    
    Example:
    'What is SQLi?' -> 'what is sqli sql injection?'
    'Explain MFA' -> 'explain mfa multi-factor authentication'
    """
    if not query:
        return query

    raw_lower = query.lower().strip()
    words = re.findall(r'\b[a-z0-9-]+\b', raw_lower)

    expansions = []
    for word in words:
        if word in CYBERSECURITY_ALIASES:
            expansion = CYBERSECURITY_ALIASES[word]
            if expansion not in raw_lower:
                expansions.append(expansion)

    if expansions:
        normalized = f"{query} {' '.join(expansions)}"
    else:
        normalized = query

    return normalized
