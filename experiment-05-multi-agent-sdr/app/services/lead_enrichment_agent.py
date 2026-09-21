"""
Lead Enrichment Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Enriches lead records with tech stack compatibility, engagement intensity, and buying intent metadata.
"""

from typing import Dict, Any

class LeadEnrichmentAgent:
    def __init__(self):
        self.agent_name = "Lead Enrichment Agent"

    def enrich_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        enriched = dict(lead)
        
        # Analyze tech stack alignment
        tech_stack = lead.get("tech_stack", [])
        high_value_tech = {"AWS", "Kubernetes", "Splunk", "Python", "PostgreSQL", "Docker"}
        tech_matches = [t for t in tech_stack if t in high_value_tech]
        
        # Engagement intensity
        signals = lead.get("engagement_signals", [])
        intensity_score = len(signals) * 25
        if "Requested Demo" in signals or "Submitted Contact Form" in signals:
            intensity_score += 30
            
        enriched["enrichment_metadata"] = {
            "tech_stack_matches": tech_matches,
            "engagement_intensity_percent": min(intensity_score, 100),
            "is_executive_role": any(r in lead.get("contact_role", "").lower() for r in ["vp", "ciso", "director", "head", "chief"]),
            "enrichment_status": "COMPLETED"
        }
        
        return enriched
