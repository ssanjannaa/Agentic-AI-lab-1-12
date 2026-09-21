"""
6-Stage Prompt Chain Orchestrator Service
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)

Executes sequential prompt chain:
Stage 1: Analysis -> Stage 2: Extraction -> Stage 3: Draft -> Stage 4: Critique -> Stage 5: Refinement -> Stage 6: Final Output
Propagates structured context from each stage down into subsequent stages.
"""

import time
import json
from typing import Dict, Any, List
from app.config import settings
from app.services.text_processor import normalize_whitespace, compute_quality_metrics
from app.services.llm_service import get_llm_provider

def execute_prompt_chain(text: str, style: str = "executive", length: str = "medium") -> Dict[str, Any]:
    """
    Executes the 6 sequential prompt stages, capturing execution timing,
    propagating inputs between stages, and assembling structured chain trace.
    """
    clean_text = normalize_whitespace(text)
    provider = get_llm_provider()

    start_total_time = time.time()
    chain_trace = []

    # =========================================================================
    # STAGE 1: DOCUMENT ANALYSIS
    # =========================================================================
    t1_start = time.time()
    analysis_data = provider.run_stage_1_analysis(clean_text)
    t1_elapsed = (time.time() - t1_start) * 1000

    chain_trace.append({
        "stage": 1,
        "name": "Document Analysis",
        "purpose": "Analyze document topic, category, domain, complexity, and structural themes",
        "inputs_consumed": ["Original Document Text"],
        "status": "completed",
        "output_preview": f"Topic: '{analysis_data.get('topic')}', Domain: '{analysis_data.get('domain')}', Complexity: '{analysis_data.get('complexity')}'",
        "execution_time_ms": round(t1_elapsed, 2)
    })

    # =========================================================================
    # STAGE 2: KEY INFORMATION EXTRACTION
    # =========================================================================
    t2_start = time.time()
    # Stage 2 explicitly consumes original text + Stage 1 analysis_data
    extraction_data = provider.run_stage_2_extraction(clean_text, analysis_data)
    t2_elapsed = (time.time() - t2_start) * 1000

    key_points = extraction_data.get("key_points", [])
    chain_trace.append({
        "stage": 2,
        "name": "Key Information Extraction",
        "purpose": "Extract key points, core concepts, terms glossary, and primary findings",
        "inputs_consumed": ["Original Document Text", "Stage 1 Document Analysis"],
        "status": "completed",
        "output_preview": f"Extracted {len(key_points)} key point(s) and {len(extraction_data.get('important_terms', []))} term(s)",
        "execution_time_ms": round(t2_elapsed, 2)
    })

    # =========================================================================
    # STAGE 3: DRAFT SUMMARY GENERATION
    # =========================================================================
    t3_start = time.time()
    # Stage 3 explicitly consumes original text + Stage 1 analysis_data + Stage 2 extraction_data + style + length
    draft_summary = provider.run_stage_3_draft(clean_text, analysis_data, extraction_data, style, length)
    t3_elapsed = (time.time() - t3_start) * 1000

    chain_trace.append({
        "stage": 3,
        "name": "Draft Summary Generation",
        "purpose": "Generate first-pass draft summary incorporating extracted info, style, and length",
        "inputs_consumed": ["Original Text", "Stage 1 Analysis", "Stage 2 Extracted Info", f"Style: {style}", f"Length: {length}"],
        "status": "completed",
        "output_preview": draft_summary[:120] + "..." if len(draft_summary) > 120 else draft_summary,
        "execution_time_ms": round(t3_elapsed, 2)
    })

    # =========================================================================
    # STAGE 4: SUMMARY CRITIQUE
    # =========================================================================
    t4_start = time.time()
    # Stage 4 explicitly consumes original text + Stage 2 extraction_data + Stage 3 draft_summary
    critique_data = provider.run_stage_4_critique(clean_text, extraction_data, draft_summary)
    t4_elapsed = (time.time() - t4_start) * 1000

    recs = critique_data.get("refinement_recommendations", [])
    chain_trace.append({
        "stage": 4,
        "name": "Summary Critique",
        "purpose": "Evaluate Stage 3 draft against Stage 2 key info for coverage, redundancy, and style compliance",
        "inputs_consumed": ["Original Text", "Stage 2 Extracted Info", "Stage 3 Draft Summary"],
        "status": "completed",
        "output_preview": f"Coverage: {critique_data.get('factual_coverage')}. Recommendations: {recs[0] if recs else 'None'}",
        "execution_time_ms": round(t4_elapsed, 2)
    })

    # =========================================================================
    # STAGE 5: SUMMARY REFINEMENT
    # =========================================================================
    t5_start = time.time()
    # Stage 5 explicitly consumes Stage 3 draft_summary + Stage 4 critique_data + Stage 2 extraction_data
    refined_summary = provider.run_stage_5_refinement(draft_summary, critique_data, extraction_data, style, length)
    t5_elapsed = (time.time() - t5_start) * 1000

    chain_trace.append({
        "stage": 5,
        "name": "Summary Refinement",
        "purpose": "Refine and rewrite Stage 3 draft by resolving Stage 4 critique points and gaps",
        "inputs_consumed": ["Stage 3 Draft Summary", "Stage 4 Critique Feedback", "Stage 2 Extracted Info"],
        "status": "completed",
        "output_preview": refined_summary[:120] + "..." if len(refined_summary) > 120 else refined_summary,
        "execution_time_ms": round(t5_elapsed, 2)
    })

    # =========================================================================
    # STAGE 6: FINAL STRUCTURED OUTPUT ASSEMBLY
    # =========================================================================
    t6_start = time.time()
    final_data = provider.run_stage_6_final(refined_summary, extraction_data, analysis_data)
    t6_elapsed = (time.time() - t6_start) * 1000

    chain_trace.append({
        "stage": 6,
        "name": "Final Structured Output",
        "purpose": "Compile final polished summary, key points, terms glossary, and metadata",
        "inputs_consumed": ["Stage 5 Refined Summary", "Stage 2 Extracted Info", "Stage 1 Analysis"],
        "status": "completed",
        "output_preview": "Final publication-ready summary package assembled",
        "execution_time_ms": round(t6_elapsed, 2)
    })

    total_time_ms = (time.time() - start_total_time) * 1000

    # Compute Quality Metrics
    metrics = compute_quality_metrics(
        original_text=clean_text,
        final_summary=final_data["final_summary"],
        key_points=final_data["key_points"],
        important_terms=final_data["important_terms"],
        total_time_ms=total_time_ms
    )

    return {
        "final_summary": final_data["final_summary"],
        "draft_summary": draft_summary,
        "key_points": final_data["key_points"],
        "important_terms": final_data["important_terms"],
        "document_analysis": analysis_data,
        "critique": critique_data,
        "metrics": metrics,
        "chain_trace": chain_trace,
        "provider": settings.LLM_PROVIDER,
        "success": True,
        "error": None
    }
