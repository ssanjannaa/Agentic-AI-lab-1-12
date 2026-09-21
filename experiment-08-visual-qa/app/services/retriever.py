"""
Visual Feature & Metadata Retriever
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
Retrieves relevant images matching text queries, labels, or category filters.
"""

import time
from typing import List, Dict, Any
from app.schemas import SearchRequest, SearchResponse, ImageSearchResult, ImageMetadata
from app.services.indexer import load_image_catalog

class VisualFeatureRetriever:
    def __init__(self):
        self.agent_name = "Visual Feature Retriever"

    def search_catalog(self, req: SearchRequest) -> SearchResponse:
        start_time = time.time()
        catalog = load_image_catalog()
        query_terms = [t.lower() for t in req.query.split() if len(t) > 2]
        
        scored_results: List[ImageSearchResult] = []

        for img in catalog:
            # Check Category Filter
            cat = img.get("category", "")
            if req.category_filter != "All" and req.category_filter.lower() not in cat.lower():
                continue

            # Calculate Feature Match Score
            matched_features = []
            score = 0.0

            title = img.get("title", "").lower()
            desc = img.get("visual_description", "").lower()
            labels = [l.lower() for l in img.get("labels", [])]

            for qt in query_terms:
                if qt in title:
                    score += 0.35
                    matched_features.append(f"Title match: '{qt}'")
                if qt in labels:
                    score += 0.40
                    matched_features.append(f"Label match: '{qt}'")
                if qt in desc:
                    score += 0.25
                    matched_features.append(f"Description match: '{qt}'")

            if not query_terms:
                score = 0.5  # Return all if empty query
                matched_features.append("Category browsing")

            if score > 0:
                scored_results.append(ImageSearchResult(
                    image=ImageMetadata(**img),
                    similarity_score=round(min(1.0, score), 2),
                    matched_features=list(set(matched_features))
                ))

        # Sort by similarity score descending
        scored_results.sort(key=lambda r: r.similarity_score, reverse=True)
        top_results = scored_results[:req.top_k]

        duration = round((time.time() - start_time) * 1000, 2)

        return SearchResponse(
            query=req.query,
            category_filter=req.category_filter,
            results_count=len(top_results),
            results=top_results,
            retrieval_duration_ms=duration
        )
