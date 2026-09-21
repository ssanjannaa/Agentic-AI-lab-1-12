"""
Synthetic Multimodal Image Catalog Generator
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
Generates structured image catalog metadata records for visual search and QA benchmarking.
"""

import json
import os

SYNTHETIC_IMAGE_CATALOG = [
    {
        "image_id": "IMG-SOC-01",
        "title": "SOC Incident Response Operations Dashboard",
        "category": "Cybersecurity Operations",
        "resolution": "1920x1080",
        "format": "PNG",
        "labels": ["soc", "dashboard", "alert", "incident", "splunk", "metrics", "monitoring"],
        "visual_description": "A high-density security operations center dashboard showing 4 alert panels, real-time network traffic spikes, and threat severity indicators (Critical red, Warning yellow).",
        "detected_objects": ["Chart Widget", "Alert Status Table", "Network Graph", "Severity Badge"],
        "metadata_properties": {
            "critical_alerts_count": 3,
            "monitored_endpoints": 1420,
            "status": "Active Triage"
        }
    },
    {
        "image_id": "IMG-NET-02",
        "title": "Enterprise Hybrid Multi-Cloud Network Architecture",
        "category": "Cloud Infrastructure",
        "resolution": "2560x1440",
        "format": "SVG",
        "labels": ["network", "cloud", "aws", "azure", "vpn", "gateway", "topology", "firewall"],
        "visual_description": "Diagram illustrating AWS VPC peered with Azure Virtual Network, connected via IPsec VPN gateway with redundant Palo Alto NextGen Firewalls.",
        "detected_objects": ["VPC Container", "VPN Tunnel Icon", "Firewall Node", "Subnet Mask"],
        "metadata_properties": {
            "vpc_subnets": 6,
            "bandwidth_gbps": 10,
            "encryption": "IPsec AES-256"
        }
    },
    {
        "image_id": "IMG-PII-03",
        "title": "Automated PII Redaction & Log Masking Pipeline",
        "category": "Data Governance",
        "resolution": "1280x720",
        "format": "JPEG",
        "labels": ["pii", "privacy", "redaction", "log", "masking", "security", "aes-256"],
        "visual_description": "Data flow diagram displaying unmasked customer raw logs entering Regex Masking Middleware and outputting redacted logs with encrypted SSN tokens.",
        "detected_objects": ["Raw Log Box", "Regex Masking Engine", "Redacted Output Box"],
        "metadata_properties": {
            "masking_rules_count": 8,
            "regex_patterns": ["Email", "Credit Card", "SSN"],
            "compliance_standard": "GDPR / HIPAA"
        }
    },
    {
        "image_id": "IMG-PQC-04",
        "title": "Post-Quantum Cryptography Hybrid Key Exchange Diagram",
        "category": "Cryptography",
        "resolution": "1920x1080",
        "format": "PNG",
        "labels": ["quantum", "cryptography", "pqc", "crystals-kyber", "tls1.3", "lattice"],
        "visual_description": "Sequence diagram of a TLS 1.3 handshake performing hybrid ECDH + CRYSTALS-Kyber key exchange between client browser and backend application gateway.",
        "detected_objects": ["Client Browser", "Gateway Node", "Kyber Key Capsule"],
        "metadata_properties": {
            "algorithm": "CRYSTALS-Kyber-768",
            "security_level": "NIST Category 3",
            "key_length_bytes": 1184
        }
    }
]

def generate_image_catalog(output_path: str = None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "images.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SYNTHETIC_IMAGE_CATALOG, f, indent=2)

    print(f"[OK] Generated {len(SYNTHETIC_IMAGE_CATALOG)} image catalog records -> {output_path}")

if __name__ == "__main__":
    generate_image_catalog()
