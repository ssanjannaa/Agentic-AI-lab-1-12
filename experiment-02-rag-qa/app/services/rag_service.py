"""
End-to-End RAG Pipeline Orchestrator Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Executes the visible 6-step RAG pipeline:
Index Check -> Query Embedding & Normalization -> Hybrid Retrieval -> Context Building -> Response Gen -> Grounded Answer
"""

from typing import Dict, Any, List
from app.config import settings
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.llm_service import get_llm_provider
from app.services.vector_store import global_vector_store

def process_rag_query(question: str, top_k: int = None) -> Dict[str, Any]:
    """
    Executes RAG pipeline, constructs grounded answer, formats retrieved sources,
    populates RAG Inspector metadata with hybrid retrieval metrics, and tracks 6 pipeline workflow steps.
    """
    if top_k is None:
        top_k = settings.DEFAULT_TOP_K

    workflow = []

    # Step 1: Document Index Check
    status = global_vector_store.get_status()
    total_chunks = status.get("chunks_indexed", 0)
    workflow.append({
        "step": "Document Index Check",
        "status": "completed",
        "details": f"Index ready. Total chunks searched: {total_chunks}"
    })

    # Step 2: Query Embedding & Normalization
    retrieval_res = retrieve_relevant_chunks(question, top_k=top_k)
    norm_query = retrieval_res.get("normalized_question", question)
    workflow.append({
        "step": "Query Embedding & Normalization",
        "status": "completed",
        "details": f"Normalized query: '{norm_query}'. Generated {settings.EMBEDDING_MODEL} dense 384-dimensional query vector."
    })

    # Step 3: Hybrid Retrieval & Relevance Filtering
    sources = retrieval_res["sources"]
    max_score = retrieval_res["max_score"]
    max_vec_score = retrieval_res.get("max_vector_score", 0.0)
    max_lex_score = retrieval_res.get("max_lexical_score", 0.0)
    is_out_of_scope = retrieval_res["is_out_of_scope"]

    workflow.append({
        "step": "Hybrid Retrieval",
        "status": "completed",
        "details": f"Retrieved top {len(sources)} chunk(s). Max Hybrid Score: {max_score} (Vector: {max_vec_score}, Lexical: {max_lex_score})"
    })

    # Step 4: Context Building
    if is_out_of_scope:
        context_details = f"Hybrid score ({max_score}) below threshold ({settings.RELEVANCE_THRESHOLD}). Flagged out-of-scope."
        sources_for_response = []
    else:
        context_details = f"Constructed grounded prompt context from {len(sources)} source document(s)."
        sources_for_response = sources

    workflow.append({
        "step": "Context Building",
        "status": "completed",
        "details": context_details
    })

    # Step 5: Response Generation
    provider = get_llm_provider()
    answer = provider.generate_grounded_answer(question, sources_for_response, is_out_of_scope)

    workflow.append({
        "step": "Response Generation",
        "status": "completed",
        "details": f"Synthesized answer using {settings.LLM_PROVIDER} provider mode"
    })

    # Step 6: Grounded Answer & Source Attribution
    workflow.append({
        "step": "Grounded Answer",
        "status": "completed",
        "details": f"Attached {len(sources_for_response)} evidence source reference(s)"
    })

    # Build RAG Inspector Metadata
    inspector = {
        "query": question,
        "normalized_query": norm_query,
        "chunks_searched": total_chunks,
        "top_k": top_k,
        "max_relevance_score": max_score,
        "vector_score": max_vec_score,
        "lexical_score": max_lex_score,
        "embedding_model": settings.EMBEDDING_MODEL,
        "vector_store": "LocalJSONVectorStore",
        "retrieval_strategy": "Hybrid (Vector + Lexical)",
        "response_mode": f"{settings.LLM_PROVIDER} (Grounded RAG)",
        "out_of_scope": is_out_of_scope
    }

    # Format Source Evidence for response
    clean_sources = [
        {
            "document": s["document"],
            "chunk_id": s["chunk_id"],
            "score": s["score"],
            "vector_score": s.get("vector_score"),
            "lexical_score": s.get("lexical_score"),
            "excerpt": s["excerpt"]
        }
        for s in sources_for_response
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": clean_sources,
        "retrieval_metadata": {
            "top_k": top_k,
            "embedding_model": settings.EMBEDDING_MODEL,
            "chunks_searched": total_chunks,
            "max_score": max_score,
            "max_vector_score": max_vec_score,
            "max_lexical_score": max_lex_score,
            "retrieval_strategy": "Hybrid (Vector + Lexical)",
            "relevance_threshold": settings.RELEVANCE_THRESHOLD
        },
        "inspector": inspector,
        "workflow": workflow,
        "provider": settings.LLM_PROVIDER,
        "success": True,
        "error": None
    }
