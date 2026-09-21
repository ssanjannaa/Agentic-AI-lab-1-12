"""
Pydantic Settings Configuration
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    LEADS_FILE_PATH: str = "data/leads.json"
    MAX_WORKFLOW_STEPS: int = 10
    MIN_QUALIFICATION_SCORE: int = 60
    PORT: int = 8004
    HOST: str = "127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
