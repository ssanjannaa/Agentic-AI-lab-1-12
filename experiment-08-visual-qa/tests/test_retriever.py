"""
Retriever Unit Tests
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from app.schemas import SearchRequest
from app.services.retriever import VisualFeatureRetriever

def test_search_catalog_dashboard_query():
    retriever = VisualFeatureRetriever()
    req = SearchRequest(query="soc dashboard metrics", category_filter="All", top_k=3)
    res = retriever.search_catalog(req)

    assert res.results_count >= 1
    top_img = res.results[0].image
    assert top_img.image_id == "IMG-SOC-01"
    assert res.results[0].similarity_score > 0.4

def test_search_catalog_category_filter():
    retriever = VisualFeatureRetriever()
    req = SearchRequest(query="cloud", category_filter="Cloud Infrastructure", top_k=3)
    res = retriever.search_catalog(req)

    assert res.results_count >= 1
    assert res.results[0].image.category == "Cloud Infrastructure"
