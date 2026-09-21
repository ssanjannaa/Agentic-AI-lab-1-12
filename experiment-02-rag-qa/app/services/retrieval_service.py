"""
Hybrid Retrieval Service (Vector + Lexical)
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Performs query normalization, dense vector embedding search, lexical phrase matching,
weighted hybrid score ranking, and relevance threshold filtering.
"""

import re
from typing import Dict, Any, List, Tuple
from app.config import settings
from app.services.embedding_service import get_embedding_engine, calculate_cosine_similarity
from app.services.vector_store import global_vector_store
from app.services.query_normalization import normalize_query

STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "of", "in", "to", "for", "does", "explain",
    "how", "and", "or", "with", "on", "at", "by", "from", "which", "do", "about"
}

# Hybrid Retrieval Weights
VECTOR_WEIGHT = 0.5
LEXICAL_WEIGHT = 0.5

def calculate_lexical_score(query: str, normalized_query: str, chunk_dict: Dict[str, Any]) -> float:
    """
    Computes normalized lexical relevance score [0.0 - 1.0] between query and document chunk.
    Evaluates term frequency, exact multi-word phrase matching, and document/section header alignment.
    """
    text_lower = chunk_dict.get("text", "").lower()
    title_lower = chunk_dict.get("title", "").lower()
    section_lower = chunk_dict.get("section", "").lower()
    full_target = f"{title_lower} {section_lower} {text_lower}"

    tokens = re.findall(r'\b[a-z0-9-]+\b', normalized_query.lower())
    content_tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]

    if not content_tokens:
        return 0.0

    # Term overlap match
    matched_terms = [t for t in content_tokens if t in full_target]
    term_match_ratio = len(matched_terms) / len(content_tokens)

    # Multi-word exact phrase matching
    phrase_score = 0.0
    if len(content_tokens) >= 2:
        phrase = " ".join(content_tokens)
        if phrase in full_target:
            phrase_score = 1.0
        else:
            subphrases = [" ".join(content_tokens[i:i+2]) for i in range(len(content_tokens) - 1)]
            submatches = [p for p in subphrases if p in full_target]
            if submatches:
                phrase_score = len(submatches) / len(subphrases)

    # Document Title & Section Header match boost
    title_section_match = 0.0
    for t in content_tokens:
        if t in title_lower or t in section_lower:
            title_section_match += 0.5
    title_section_match = min(1.0, title_section_match)

    # Weighted lexical combination
    lexical = (0.5 * term_match_ratio) + (0.3 * phrase_score) + (0.2 * title_section_match)
    return min(1.0, max(0.0, float(lexical)))


def retrieve_relevant_chunks(question: str, top_k: int = None) -> Dict[str, Any]:
    """
    Executes Hybrid Retrieval (Vector Similarity + Lexical Phrase Matching):
    1. Normalizes question aliases/acronyms.
    2. Embeds query & computes Cosine Similarity across vector store entries.
    3. Computes Lexical Phrase Relevance scores across entries.
    4. Computes Weighted Hybrid Score: (vector_weight * vector_score) + (lexical_weight * lexical_score).
    5. Filters results by RELEVANCE_THRESHOLD to enforce out-of-KB safety.
    """
    if top_k is None:
        top_k = settings.DEFAULT_TOP_K

    # Step 1: Query Normalization
    norm_query = normalize_query(question)

    # Step 2: Vector Embedding & Search
    embedding_engine = get_embedding_engine()
    query_vector = embedding_engine.embed_text(norm_query)

    if not global_vector_store.index_data.get("entries"):
        global_vector_store.build_index()

    entries = global_vector_store.index_data.get("entries", [])

    scored_entries = []
    for entry in entries:
        chunk_vector = entry.get("vector", [])
        vec_score = calculate_cosine_similarity(query_vector, chunk_vector)
        lex_score = calculate_lexical_score(question, norm_query, entry)

        hybrid_score = (VECTOR_WEIGHT * vec_score) + (LEXICAL_WEIGHT * lex_score)

        scored_entries.append({
            "entry": entry,
            "hybrid_score": float(hybrid_score),
            "vector_score": float(vec_score),
            "lexical_score": float(lex_score)
        })

    # Sort descending by hybrid_score
    scored_entries.sort(key=lambda x: x["hybrid_score"], reverse=True)
    top_candidates = scored_entries[:top_k]

    sources = []
    max_hybrid_score = 0.0
    top_vector_score = 0.0
    top_lexical_score = 0.0

    if top_candidates:
        max_hybrid_score = top_candidates[0]["hybrid_score"]
        top_vector_score = top_candidates[0]["vector_score"]
        top_lexical_score = top_candidates[0]["lexical_score"]

    for item in top_candidates:
        entry = item["entry"]
        h_score = item["hybrid_score"]
        v_score = item["vector_score"]
        l_score = item["lexical_score"]

        raw_text = entry.get("text", "")
        excerpt = raw_text[:220] + "..." if len(raw_text) > 220 else raw_text

        sources.append({
            "document": entry.get("title", ""),
            "chunk_id": entry.get("chunk_id", ""),
            "score": round(float(h_score), 4),
            "vector_score": round(float(v_score), 4),
            "lexical_score": round(float(l_score), 4),
            "excerpt": excerpt,
            "full_text": raw_text
        })

    # Check if max hybrid score meets relevance threshold
    is_out_of_scope = (max_hybrid_score < settings.RELEVANCE_THRESHOLD)

    return {
        "question": question,
        "normalized_question": norm_query,
        "sources": sources,
        "max_score": round(float(max_hybrid_score), 4),
        "max_vector_score": round(float(top_vector_score), 4),
        "max_lexical_score": round(float(top_lexical_score), 4),
        "is_out_of_scope": is_out_of_scope,
        "chunks_searched": len(entries),
        "top_k": top_k,
        "retrieval_strategy": "Hybrid (Vector + Lexical)"
    }
