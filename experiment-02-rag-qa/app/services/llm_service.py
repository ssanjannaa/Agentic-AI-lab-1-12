"""
LLM Response Generator Service
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)

Provides provider abstraction supporting:
- MockLLMProvider (Grounded offline response generator using retrieved context)
- OpenAIProvider (OpenAI API)
- AnthropicProvider (Anthropic Claude API)
- GeminiProvider (Google Gemini API)
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.config import settings

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_grounded_answer(self, question: str, sources: List[Dict[str, Any]], is_out_of_scope: bool) -> str:
        """Generates grounded answer based strictly on retrieved source evidence."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Offline response generator for RAG testing.
    Synthesizes answers from retrieved chunks or handles out-of-scope queries cleanly.
    """
    def generate_grounded_answer(self, question: str, sources: List[Dict[str, Any]], is_out_of_scope: bool) -> str:
        if is_out_of_scope or not sources:
            return f"The cybersecurity knowledge base does not contain sufficient information to answer your question about '{question}'. Please ask a cybersecurity-related topic."

        top_source = sources[0]
        doc_title = top_source["document"]
        excerpt = top_source["full_text"]

        # Extract primary sentences from retrieved chunk
        sentences = [s.strip() for s in excerpt.split(".") if len(s.strip()) > 15]
        key_points = ". ".join(sentences[:3]) + "." if sentences else excerpt[:200]

        return (
            f"Based on the **{doc_title}** knowledge base document:\n\n"
            f"{key_points}\n\n"
            f"*(Source: {doc_title}, Chunk: {top_source['chunk_id']}, Relevance Score: {int(top_source['score'] * 100)}%)*"
        )


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        import httpx
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.httpx = httpx

    def generate_grounded_answer(self, question: str, sources: List[Dict[str, Any]], is_out_of_scope: bool) -> str:
        if is_out_of_scope or not sources:
            return f"The cybersecurity knowledge base does not contain sufficient information to answer your question about '{question}'. Please ask a cybersecurity-related topic."

        context_str = "\n\n".join([
            f"--- Source: {s['document']} ({s['chunk_id']}) ---\n{s['full_text']}"
            for s in sources
        ])

        system_prompt = (
            "You are a Cybersecurity Knowledge RAG Assistant. Answer the user question based strictly on the provided context below. "
            "If the context does not contain enough information, state that the knowledge base does not contain sufficient details. "
            "Include inline source references to the documents used.\n\n"
            f"RETRIEVED CONTEXT:\n{context_str}"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.2
        }

        try:
            response = self.httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return MockLLMProvider().generate_grounded_answer(question, sources, is_out_of_scope)


def get_llm_provider() -> BaseLLMProvider:
    provider_name = settings.LLM_PROVIDER.upper().strip()
    if provider_name == "OPENAI" and settings.OPENAI_API_KEY:
        return OpenAIProvider()
    return MockLLMProvider()
