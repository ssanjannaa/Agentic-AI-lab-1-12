"""
Application Configuration Settings
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "knowledge_base")
INDEX_DIR = os.path.join(BASE_DIR, "index")
DEFAULT_INDEX_PATH = os.path.join(INDEX_DIR, "vector_index.json")

class Settings(BaseSettings):
    APP_TITLE: str = "Cybersecurity Knowledge RAG Assistant"
    APP_VERSION: str = "1.0.0"
    COURSE_CODE: str = "MR23-1CS0436"
    
    # LLM Provider: MOCK | OPENAI | ANTHROPIC | GEMINI
    LLM_PROVIDER: str = "MOCK"
    
    # Model Configurations
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "local-dense-384"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # RAG Parameters
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 60
    DEFAULT_TOP_K: int = 4
    RELEVANCE_THRESHOLD: float = 0.25
    
    # Storage Paths
    KNOWLEDGE_BASE_DIR: str = DATA_DIR
    INDEX_PATH: str = DEFAULT_INDEX_PATH
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8001
    DEBUG: bool = True

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
