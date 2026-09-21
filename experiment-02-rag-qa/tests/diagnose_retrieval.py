"""
Retrieval Quality Diagnostic Script
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

import os
import sys

# Ensure app is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.retrieval_service import retrieve_relevant_chunks
from app.config import settings
from app.services.vector_store import global_vector_store

# Build/refresh index first
global_vector_store.build_index()

queries = [
    "What is SQL injection?",
    "What is SQLi?",
    "What is phishing?",
    "What is ransomware?",
    "What does a firewall do?",
    "Explain MFA",
    "What are the phases of incident response?",
    "What is security monitoring?",
    "What is the capital of France?"
]

print("=== RETRIEVAL DIAGNOSTIC REPORT ===")
print(f"Current RELEVANCE_THRESHOLD: {settings.RELEVANCE_THRESHOLD}\n")

for i, q in enumerate(queries, 1):
    res = retrieve_relevant_chunks(q, top_k=4)
    sources = res["sources"]
    max_score = res["max_score"]
    is_out = res["is_out_of_scope"]
    
    print(f"[{i}] Query: '{q}'")
    print(f"  Max Score: {max_score:.4f}")
    print(f"  Relevance Decision: {'REJECTED (Out of KB)' if is_out else 'ACCEPTED (In KB)'}")
    print(f"  Out of KB Flag: {is_out}")
    print(f"  Top 4 Retrieved Chunks:")
    if sources:
        for idx, src in enumerate(sources, 1):
            print(f"    Rank {idx}: [{src['score']:.4f}] Doc: '{src['document']}' | Chunk ID: {src['chunk_id']}")
    else:
        print("    (No sources retrieved)")
    print("-" * 70)

# Specific check for SQL injection
sql_res = retrieve_relevant_chunks("What is SQL injection?", top_k=10)
sql_sources = sql_res["sources"]
doc_04_found = False
doc_04_rank = None
doc_04_score = None
for idx, src in enumerate(sql_sources, 1):
    if "Web Application Security" in src["document"] or "04" in src["chunk_id"]:
        doc_04_found = True
        doc_04_rank = idx
        doc_04_score = src["score"]
        break

print("\n=== SPECIFIC SQL INJECTION ANALYSIS ===")
print(f"Query: 'What is SQL injection?'")
print(f"04_web_application_security.md appeared: {doc_04_found}")
if doc_04_found:
    print(f"Rank: #{doc_04_rank}")
    print(f"Similarity Score: {doc_04_score:.4f}")
else:
    print("04_web_application_security.md was NOT found in top 10 chunks.")
