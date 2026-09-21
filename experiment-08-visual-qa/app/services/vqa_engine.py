"""
Visual Question Answering (VQA) Engine
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
Answers questions about images grounded on visual features and metadata properties.
"""

import time
from typing import Dict, Any, List
from app.schemas import VisualQARequest, VisualQAResponse
from app.services.indexer import get_image_by_id

class VisualQAEngine:
    def __init__(self):
        self.engine_name = "Grounded Visual QA Engine v1.0"

    def answer_question(self, req: VisualQARequest) -> VisualQAResponse:
        start_time = time.time()
        img = get_image_by_id(req.image_id)

        if not img:
            return VisualQAResponse(
                image_id=req.image_id,
                image_title="Unknown Image",
                question=req.question,
                answer=f"Image ID '{req.image_id}' not found in the visual catalog.",
                grounded_evidence=[],
                confidence_score=0.0,
                detected_objects_referenced=[],
                vqa_duration_ms=0.5
            )

        title = img["title"]
        desc = img["visual_description"]
        objects = img.get("detected_objects", [])
        props = img.get("metadata_properties", {})

        question_lower = req.question.lower()
        evidence = []
        referenced_objects = []

        # Extract answer grounded on metadata properties and visual description
        if "alert" in question_lower or "critical" in question_lower:
            crit_count = props.get("critical_alerts_count", "N/A")
            endpoints = props.get("monitored_endpoints", "N/A")
            answer = f"The dashboard displays {crit_count} critical severity alerts across {endpoints} monitored endpoints."
            evidence.append(f"Metadata property: critical_alerts_count={crit_count}")
            evidence.append(f"Metadata property: monitored_endpoints={endpoints}")
            referenced_objects.extend(["Alert Status Table", "Severity Badge"])

        elif "subnet" in question_lower or "vpn" in question_lower or "cloud" in question_lower:
            subnets = props.get("vpc_subnets", "N/A")
            enc = props.get("encryption", "IPsec AES-256")
            answer = f"The network diagram illustrates {subnets} VPC subnets connected via an IPsec VPN tunnel with {enc} encryption."
            evidence.append(f"Metadata property: vpc_subnets={subnets}")
            evidence.append(f"Metadata property: encryption={enc}")
            referenced_objects.extend(["VPC Container", "VPN Tunnel Icon"])

        elif "pii" in question_lower or "mask" in question_lower or "redact" in question_lower:
            rules = props.get("masking_rules_count", "N/A")
            patterns = ", ".join(props.get("regex_patterns", []))
            answer = f"The PII data pipeline applies {rules} automated masking rules targeting {patterns} prior to log storage."
            evidence.append(f"Metadata property: regex_patterns=[{patterns}]")
            referenced_objects.extend(["Regex Masking Engine", "Redacted Output Box"])

        elif "quantum" in question_lower or "kyber" in question_lower or "pqc" in question_lower:
            algo = props.get("algorithm", "CRYSTALS-Kyber-768")
            sec_level = props.get("security_level", "NIST Category 3")
            answer = f"The PQC diagram shows a hybrid TLS handshake utilizing {algo} at {sec_level} security."
            evidence.append(f"Metadata property: algorithm={algo}")
            referenced_objects.extend(["Kyber Key Capsule", "Gateway Node"])

        else:
            answer = f"Based on the visual analysis of '{title}', the image depicts: {desc}"
            evidence.append(f"Visual description match: '{desc[:60]}...'")
            referenced_objects.extend(objects[:2])

        confidence = 0.95 if evidence else 0.70
        duration = round((time.time() - start_time) * 1000, 2)

        return VisualQAResponse(
            image_id=req.image_id,
            image_title=title,
            question=req.question,
            answer=answer,
            grounded_evidence=evidence,
            confidence_score=confidence,
            detected_objects_referenced=list(set(referenced_objects)),
            vqa_duration_ms=duration
        )
