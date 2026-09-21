# Experiment 02 — Screenshots & Visual Artifacts Directory

**Course Code:** MR23-1CS0436
**Experiment Name:** RAG-Based Question Answering System

---

## 📌 Overview

This directory stores verified visual evidence and runtime application screenshots demonstrating the **Cybersecurity Knowledge RAG Assistant** web application.

---

## 📷 Verified Verification Screenshots

The following 5 high-resolution screenshot artifacts document the application's visual flow, hybrid retrieval diagnostics, and safety thresholding:

1. **`01-home-dashboard.png`**
   - Captures the initial Chatbot UI with the header title, loaded Knowledge Base Status Bar (9 Documents, 37 Chunks), RAG pipeline progress bar, and sample question chips.
2. **`02-rag-query-retrieval.png`**
   - Captures a successful execution of a natural language cybersecurity question (e.g., *"What is phishing?"*).
   - Demonstrates the active RAG pipeline bar, grounded answer text, and the **Retrieved Sources Panel** displaying source documents, chunk IDs, and relevance scores.
3. **`03-rag-inspector-diagnostics.png`**
   - Captures an expanded **RAG Inspector Diagnostics** panel showing chunks searched, Top-K, maximum cosine similarity score, and vector store metrics.
4. **`04-out-of-knowledge-base-handling.png`**
   - Captures an out-of-knowledge-base query (e.g., *"What is the capital of France?"*) demonstrating proper threshold filtering and clean out-of-scope response handling.
5. **`05-sql-injection-retrieval.png`**
   - Captures verified retrieval for *"What is SQL Injection?"* demonstrating Rank #1 match (`Web Application Security`), grounded answer text, and hybrid vector+lexical scoring metrics.

---

## 🎨 Asset Naming Standard
- Format: Lowercase hyphenated string (e.g., `01-home-dashboard.png`).
- Format type: `.png`.
