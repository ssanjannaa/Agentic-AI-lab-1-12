"""
Application Configuration Settings
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(BASE_DIR, "data", "samples")

class Settings(BaseSettings):
    APP_TITLE: str = "Agentic Document Summarization Studio"
    APP_VERSION: str = "1.0.0"
    COURSE_CODE: str = "MR23-1CS0436"
    
    # LLM Provider: MOCK | OPENAI | ANTHROPIC | GEMINI
    LLM_PROVIDER: str = "MOCK"
    
    # Model Configurations
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Default Summarization Options
    DEFAULT_SUMMARY_STYLE: str = "executive"
    DEFAULT_SUMMARY_LENGTH: str = "medium"
    
    SAMPLES_DIR: str = SAMPLES_DIR
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8002
    DEBUG: bool = True

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
