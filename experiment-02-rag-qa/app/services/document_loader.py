"""
Document Loader Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Parses local Markdown files from the knowledge base directory.
"""

import os
import glob
from typing import List, Dict, Any
from app.config import settings

class Document:
    def __init__(self, doc_id: str, filename: str, title: str, content: str):
        self.doc_id = doc_id
        self.filename = filename
        self.title = title
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "title": self.title,
            "content": self.content
        }

def load_knowledge_base_documents(kb_dir: str = None) -> List[Document]:
    """
    Scans the knowledge base directory, reads Markdown documents,
    and extracts titles and contents into Document objects.
    """
    if kb_dir is None:
        kb_dir = settings.KNOWLEDGE_BASE_DIR

    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir, exist_ok=True)
        return []

    filepaths = sorted(glob.glob(os.path.join(kb_dir, "*.md")))
    documents = []

    for idx, fpath in enumerate(filepaths, 1):
        filename = os.path.basename(fpath)
        doc_id = f"doc_{idx:02d}"

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Extract title from first line (# Title)
        title = filename.replace(".md", "").replace("_", " ").title()
        lines = content.split("\n")
        if lines and lines[0].startswith("# "):
            title = lines[0].replace("# ", "").strip()

        documents.append(Document(
            doc_id=doc_id,
            filename=filename,
            title=title,
            content=content
        ))

    return documents
