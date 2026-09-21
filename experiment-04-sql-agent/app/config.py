"""
Pydantic Settings Configuration
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    DATABASE_PATH: str = "data/company.db"
    MAX_AGENT_ITERATIONS: int = 8
    DEFAULT_ROW_LIMIT: int = 50
    PORT: int = 8003
    HOST: str = "127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
