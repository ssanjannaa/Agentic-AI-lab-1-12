"""
Policy Data Loader Service
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

import json
import os
from typing import List, Dict, Any, Optional
from app.config import settings

def _resolve_path(rel_path: str) -> str:
    if os.path.isabs(rel_path):
        return rel_path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, rel_path)

def load_policies() -> List[Dict[str, Any]]:
    p_path = _resolve_path(settings.POLICIES_FILE_PATH)
    if not os.path.exists(p_path):
        from data.seed_policies import generate_policy_data
        generate_policy_data(p_path)

    with open(p_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_scenarios() -> List[Dict[str, Any]]:
    s_path = _resolve_path(settings.SCENARIOS_FILE_PATH)
    if not os.path.exists(s_path):
        from data.seed_policies import generate_policy_data
        generate_policy_data(scenarios_path=s_path)

    with open(s_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_policy_by_id(policy_id: str) -> Optional[Dict[str, Any]]:
    policies = load_policies()
    for p in policies:
        if p["policy_id"] == policy_id:
            return p
    return None
