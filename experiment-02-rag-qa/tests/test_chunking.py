"""
Text Chunking Unit Tests
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from app.services.document_loader import Document
from app.services.chunking_service import chunk_document

def test_chunk_document_size_and_metadata():
    sample_text = "Word " * 250  # 1250 characters
    doc = Document("doc_test", "test.md", "Test Doc", sample_text)
    chunks = chunk_document(doc, chunk_size=400, chunk_overlap=60)
    
    assert len(chunks) >= 3
    for chunk in chunks:
        assert chunk.doc_id == "doc_test"
        assert chunk.title == "Test Doc"
        assert len(chunk.text) <= 450
        assert chunk.chunk_id.startswith("doc_test_chunk_")
