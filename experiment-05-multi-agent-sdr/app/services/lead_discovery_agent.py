"""
Lead Discovery Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Responsible for searching, filtering, and discovering synthetic B2B target leads.
"""

import json
import os
from typing import List, Dict, Any
from app.config import settings

def load_all_leads() -> List[Dict[str, Any]]:
    leads_path = settings.LEADS_FILE_PATH
    if not os.path.isabs(leads_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        leads_path = os.path.join(base_dir, leads_path)

    if not os.path.exists(leads_path):
        from data.seed_leads import generate_leads_json
        generate_leads_json(leads_path)

    with open(leads_path, "r", encoding="utf-8") as f:
        return json.load(f)

class LeadDiscoveryAgent:
    def __init__(self):
        self.agent_name = "Lead Discovery Agent"

    def discover_leads(self, target_industry: str = "All", target_region: str = "All") -> List[Dict[str, Any]]:
        all_leads = load_all_leads()
        discovered = []

        for lead in all_leads:
            match_ind = (target_industry == "All" or target_industry.lower() in lead.get("industry", "").lower())
            match_reg = (target_region == "All" or target_region.lower() in lead.get("region", "").lower())

            if match_ind and match_reg:
                discovered.append(lead)

        return discovered
