"""
RAG Retrieval Specialist Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Tuple
from app.schemas import EvidenceItem, AgentStepTrace
from app.services.rag_engine import rag_engine

class RetrievalAgent:
    def __init__(self):
        self.agent_name = "RetrievalAgent"

    def execute_retrieval(self, query: str, top_k: int = 3, step_id: int = 2) -> Tuple[List[EvidenceItem], AgentStepTrace]:
        start = time.time()
        evidence_items = rag_engine.retrieve(query, top_k=top_k)

        duration_ms = round((time.time() - start) * 1000, 2)
        top_doc = evidence_items[0].document_name if evidence_items else "None"
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Retrieve Local RAG Evidence",
            input_summary=f"Query: {query[:60]}",
            output_summary=f"Retrieved {len(evidence_items)} chunks. Top source: {top_doc}",
            duration_ms=duration_ms,
            status="COMPLETED"
        )

        return evidence_items, trace
