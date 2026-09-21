"""
Heading-Aware Text Chunking Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Splits documents into overlapping chunks with metadata preservation and active heading context.
"""

import re
from typing import List, Dict, Any
from app.services.document_loader import Document
from app.config import settings

class Chunk:
    def __init__(self, chunk_id: str, doc_id: str, source: str, title: str, start_char: int, end_char: int, text: str, section: str = ""):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.source = source
        self.title = title
        self.section = section
        self.start_char = start_char
        self.end_char = end_char
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "source": self.source,
            "title": self.title,
            "section": self.section,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "text": self.text
        }

def _get_active_section(full_text: str, current_pos: int) -> str:
    """Extracts the most recent Markdown heading prior to current_pos."""
    prefix = full_text[:current_pos]
    lines = prefix.splitlines()
    for line in reversed(lines):
        line_s = line.strip()
        if line_s.startswith("#"):
            return re.sub(r'^#+\s*', '', line_s)
    return ""

def chunk_document(doc: Document, chunk_size: int = None, chunk_overlap: int = None) -> List[Chunk]:
    """
    Splits a single document into overlapping text chunks with preserved metadata
    and prepended heading/document context for enhanced retrieval quality.
    """
    if chunk_size is None:
        chunk_size = settings.CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = settings.CHUNK_OVERLAP

    text = doc.content
    chunks = []
    text_len = len(text)

    if text_len == 0:
        return chunks

    start = 0
    chunk_num = 1

    while start < text_len:
        end = start + chunk_size
        
        # Adjust end to avoid splitting words if possible
        if end < text_len:
            space_idx = text.rfind(" ", start, end)
            if space_idx > start + (chunk_size // 2):
                end = space_idx

        chunk_body = text[start:end].strip()
        if chunk_body:
            section = _get_active_section(text, start)
            context_header = f"[{doc.title} - {section}]\n" if section else f"[{doc.title}]\n"
            full_chunk_text = context_header + chunk_body

            chunk_id = f"{doc.doc_id}_chunk_{chunk_num:02d}"
            chunks.append(Chunk(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                source=doc.title,
                title=doc.title,
                section=section,
                start_char=start,
                end_char=end,
                text=full_chunk_text
            ))
            chunk_num += 1

        start = end - chunk_overlap if end < text_len else text_len

    return chunks

def chunk_all_documents(documents: List[Document], chunk_size: int = None, chunk_overlap: int = None) -> List[Chunk]:
    """
    Chunks a list of Document objects.
    """
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc, chunk_size, chunk_overlap)
        all_chunks.extend(doc_chunks)
    return all_chunks
