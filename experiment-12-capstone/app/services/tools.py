"""
Safe Defensive Cybersecurity Tools
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import re
import json
import os
import time
from typing import Dict, List, Any
from app.config import settings
from app.services.rag_engine import rag_engine

class KnowledgeSearchTool:
    @staticmethod
    def execute(query: str, top_k: int = 3) -> Dict[str, Any]:
        start = time.time()
        results = rag_engine.retrieve(query, top_k=top_k)
        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "tool_name": "KnowledgeSearchTool",
            "query": query,
            "results_count": len(results),
            "evidence": [item.dict() for item in results],
            "duration_ms": duration_ms
        }

class IOCParserTool:
    @staticmethod
    def execute(raw_text: str) -> Dict[str, Any]:
        start = time.time()
        
        # Regex patterns for IOC extraction
        ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|gov|edu|info|co|xyz|biz|ru|cn)\b'
        cve_pattern = r'\bCVE-\d{4}-\d{4,7}\b'
        sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
        md5_pattern = r'\b[a-fA-F0-9]{32}\b'
        url_pattern = r'https?://[^\s<>"]+'

        ips = sorted(list(set(re.findall(ip_pattern, raw_text))))
        # Filter out common local/loopback IPs if needed, keep for forensic log display
        domains = sorted(list(set(re.findall(domain_pattern, raw_text.lower()))))
        cves = sorted(list(set(re.findall(cve_pattern, raw_text, re.IGNORECASE))))
        hashes = sorted(list(set(re.findall(sha256_pattern, raw_text) + re.findall(md5_pattern, raw_text))))
        urls = sorted(list(set(re.findall(url_pattern, raw_text))))

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "tool_name": "IOCParserTool",
            "extracted_iocs": {
                "ip_addresses": ips,
                "domains": domains,
                "cve_ids": cves,
                "file_hashes": hashes,
                "urls": urls
            },
            "total_extracted": len(ips) + len(domains) + len(cves) + len(hashes) + len(urls),
            "duration_ms": duration_ms
        }

class RiskCalculatorTool:
    @staticmethod
    def execute(impact_score: float, likelihood_score: float, confidence: float = 0.8, asset_criticality: float = 1.0) -> Dict[str, Any]:
        start = time.time()
        
        # Risk Score Formula: Risk = (Impact * Likelihood * Asset Criticality) * Confidence
        # Scaled to 0.0 - 10.0 range
        raw_score = (impact_score * likelihood_score * asset_criticality) * confidence
        risk_score = round(min(max(raw_score, 0.0), 10.0), 2)

        if risk_score >= 8.0:
            severity = "CRITICAL"
        elif risk_score >= 6.0:
            severity = "HIGH"
        elif risk_score >= 3.5:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "tool_name": "RiskCalculatorTool",
            "risk_score": risk_score,
            "severity_level": severity,
            "formula_parameters": {
                "impact_score": impact_score,
                "likelihood_score": likelihood_score,
                "confidence_level": confidence,
                "asset_criticality": asset_criticality
            },
            "duration_ms": duration_ms
        }

class MITRELookupTool:
    @staticmethod
    def execute(category: str) -> Dict[str, Any]:
        start = time.time()
        mitre_file = settings.MITRE_FILE
        mapping_data = {}
        if os.path.exists(mitre_file):
            with open(mitre_file, "r", encoding="utf-8") as f:
                mapping_data = json.load(f)

        category_data = mapping_data.get(category, {
            "tactic": "General Cyber Defense",
            "techniques": [
                {"id": "T1078", "name": "Valid Accounts", "description": "Abuse of existing credentials."},
                {"id": "T1190", "name": "Exploit Public-Facing Application", "description": "Web service vulnerability exploitation."}
            ],
            "defensive_controls": ["Patch Management", "Perimeter Firewalls", "MFA Enforcement"]
        })

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "tool_name": "MITRELookupTool",
            "category": category,
            "tactic": category_data.get("tactic", "General"),
            "techniques": category_data.get("techniques", []),
            "defensive_controls": category_data.get("defensive_controls", []),
            "duration_ms": duration_ms
        }

class IncidentTimelineBuilderTool:
    @staticmethod
    def execute(raw_logs: List[str]) -> Dict[str, Any]:
        start = time.time()
        timeline_entries = []

        for idx, log in enumerate(raw_logs):
            # Extract timestamp or default
            time_match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?', log)
            timestamp = time_match.group(0) if time_match else f"Event-Step-{idx+1}"
            
            timeline_entries.append({
                "sequence": idx + 1,
                "timestamp": timestamp,
                "event_detail": log.strip()
            })

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "tool_name": "IncidentTimelineBuilderTool",
            "total_events": len(timeline_entries),
            "timeline": timeline_entries,
            "duration_ms": duration_ms
        }
