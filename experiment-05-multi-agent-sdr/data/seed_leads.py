"""
Synthetic Lead Dataset Generator
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Generates educational B2B lead profiles for agent qualification and outreach benchmarking.
"""

import json
import os

SYNTHETIC_LEADS = [
    {
        "id": "LEAD-101",
        "contact_name": "Sarah Jenkins",
        "contact_role": "VP of Infrastructure",
        "email": "sarah.jenkins@cloudnexus.io",
        "company_name": "CloudNexus Tech",
        "industry": "Cloud Infrastructure",
        "company_size": "500-1000",
        "region": "North America",
        "business_need": "Automating multi-cloud orchestration and reducing AWS cloud spend overrun",
        "engagement_signals": ["Downloaded Whitepaper", "Attended Webinar", "Visited Pricing Page 3x"],
        "budget_band": "$50,000 - $100,000",
        "tech_stack": ["AWS", "Kubernetes", "Terraform", "Python"],
        "fit_indicators": {"tech_match": True, "decision_maker": True, "urgency": "High"}
    },
    {
        "id": "LEAD-102",
        "contact_name": "Marcus Vance",
        "contact_role": "Chief Information Security Officer",
        "email": "marcus.vance@securesphere.com",
        "company_name": "SecureSphere Cyber",
        "industry": "Cybersecurity",
        "company_size": "250-500",
        "region": "Europe (UK)",
        "business_need": "Automated SOC incident response triage and RAG-based compliance policy checking",
        "engagement_signals": ["Requested Demo", "Submitted Contact Form"],
        "budget_band": "$100,000+",
        "tech_stack": ["Splunk", "CrowdStrike", "Python", "FastAPI"],
        "fit_indicators": {"tech_match": True, "decision_maker": True, "urgency": "Critical"}
    },
    {
        "id": "LEAD-103",
        "contact_name": "Dr. Aris Thorne",
        "contact_role": "Head of Data Science",
        "email": "aris.thorne@biomedgen.org",
        "company_name": "BioMedGen Analytics",
        "industry": "Healthcare & Biotech",
        "company_size": "100-250",
        "region": "North America",
        "business_need": "Accelerating clinical trial literature synthesis using agentic LLM pipelines",
        "engagement_signals": ["Downloaded Technical Case Study"],
        "budget_band": "$30,000 - $50,000",
        "tech_stack": ["PyTorch", "Hugging Face", "PostgreSQL"],
        "fit_indicators": {"tech_match": True, "decision_maker": False, "urgency": "Medium"}
    },
    {
        "id": "LEAD-104",
        "contact_name": "Elena Rostova",
        "contact_role": "Director of E-Commerce Engineering",
        "email": "elena.rostova@retailpulse.de",
        "company_name": "RetailPulse Global",
        "industry": "E-Commerce & Retail",
        "company_size": "1000+",
        "region": "Europe (Germany)",
        "business_need": "Real-time AI customer support and automated order exception resolution",
        "engagement_signals": ["Visited Home Page", "Viewed Blog Post"],
        "budget_band": "$15,000 - $30,000",
        "tech_stack": ["Shopify Plus", "React", "Node.js"],
        "fit_indicators": {"tech_match": False, "decision_maker": True, "urgency": "Low"}
    },
    {
        "id": "LEAD-105",
        "contact_name": "David Chen",
        "contact_role": "Engineering Lead",
        "email": "david.chen@fintechlabs.asia",
        "company_name": "FinTechLabs Asia",
        "industry": "Financial Technology",
        "company_size": "50-100",
        "region": "Asia-Pacific",
        "business_need": "Automating SQL data extraction and agentic customer portfolio reporting",
        "engagement_signals": ["Downloaded API Docs", "Attended Product Demo"],
        "budget_band": "$50,000 - $100,000",
        "tech_stack": ["PostgreSQL", "Go", "Docker"],
        "fit_indicators": {"tech_match": True, "decision_maker": False, "urgency": "High"}
    },
    {
        "id": "LEAD-106",
        "contact_name": "Rachel Adams",
        "contact_role": "VP of Product Development",
        "email": "rachel.adams@edulearn.net",
        "company_name": "EduLearn Systems",
        "industry": "EdTech",
        "company_size": "20-50",
        "region": "North America",
        "business_need": "Exploring general AI tools for course generation",
        "engagement_signals": ["Unsubscribed from Newsletter"],
        "budget_band": "< $10,000",
        "tech_stack": ["WordPress", "PHP"],
        "fit_indicators": {"tech_match": False, "decision_maker": True, "urgency": "Low"}
    }
]

def generate_leads_json(output_path: str = None) -> str:
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "leads.json")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SYNTHETIC_LEADS, f, indent=2)
    
    print(f"[OK] Generated {len(SYNTHETIC_LEADS)} synthetic SDR lead records -> {output_path}")
    return output_path

if __name__ == "__main__":
    generate_leads_json()
