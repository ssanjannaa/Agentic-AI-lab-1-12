"""
Local Deterministic RAG Retrieval Engine
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import os
import re
import math
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.schemas import EvidenceItem

class RAGEngine:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.chunks: List[Dict[str, Any]] = []
        self.index_loaded = False
        self._load_and_index_documents()

    def _load_and_index_documents(self):
        if not os.path.exists(settings.KNOWLEDGE_BASE_DIR):
            return

        kb_files = [f for f in os.listdir(settings.KNOWLEDGE_BASE_DIR) if f.endswith(".md")]
        self.chunks = []
        self.documents = []

        for doc_name in kb_files:
            file_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, doc_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.documents.append({"doc_name": doc_name, "content": content})
            
            # Simple header/paragraph chunking
            sections = re.split(r'\n(?=##?\s)', content)
            for idx, section in enumerate(sections):
                cleaned_text = section.strip()
                if not cleaned_text:
                    continue

                # Extract topics / keywords from section headers
                lines = cleaned_text.splitlines()
                header = lines[0].replace("#", "").strip() if lines else "General"
                
                # Split large sections into smaller chunks if necessary
                words = cleaned_text.split()
                chunk_size = settings.CHUNK_SIZE
                overlap = settings.CHUNK_OVERLAP

                if len(words) <= chunk_size:
                    self.chunks.append({
                        "doc_name": doc_name,
                        "chunk_id": f"{doc_name}-chunk-{idx}",
                        "header": header,
                        "content": cleaned_text,
                        "words": set(re.findall(r'\b\w+\b', cleaned_text.lower()))
                    })
                else:
                    sub_idx = 0
                    for i in range(0, len(words), chunk_size - overlap):
                        sub_words = words[i:i + chunk_size]
                        sub_text = " ".join(sub_words)
                        self.chunks.append({
                            "doc_name": doc_name,
                            "chunk_id": f"{doc_name}-chunk-{idx}-{sub_idx}",
                            "header": header,
                            "content": sub_text,
                            "words": set(re.findall(r'\b\w+\b', sub_text.lower()))
                        })
                        sub_idx += 1

        self.index_loaded = True

    def retrieve(self, query: str, top_k: int = 3) -> List[EvidenceItem]:
        if not self.chunks:
            return []

        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        # Filter out common stop words
        stop_words = {"a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "is", "are", "this", "that", "it"}
        filtered_query = {w for w in query_words if w not in stop_words and len(w) > 2}

        scored_chunks: List[Tuple[float, Dict[str, Any]]] = []

        for chunk in self.chunks:
            chunk_words = chunk["words"]
            if not chunk_words or not filtered_query:
                score = 0.0
            else:
                intersection = filtered_query.intersection(chunk_words)
                # Jaccard / Term frequency similarity
                score = float(len(intersection)) / (math.sqrt(len(filtered_query)) * math.sqrt(len(chunk_words)) + 1e-5)
                
                # Bonus for title/header matches
                header_words = set(re.findall(r'\b\w+\b', chunk["header"].lower()))
                if filtered_query.intersection(header_words):
                    score += 0.25

            if score > 0.0:
                scored_chunks.append((score, chunk))

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results: List[EvidenceItem] = []
        for score, chunk in scored_chunks[:top_k]:
            results.append(EvidenceItem(
                document_name=chunk["doc_name"],
                chunk_id=chunk["chunk_id"],
                content=chunk["content"],
                relevance_score=round(min(score, 1.0), 4),
                topics=[chunk["header"]]
            ))

        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_documents": len(self.documents),
            "total_indexed_chunks": len(self.chunks)
        }

rag_engine = RAGEngine()
