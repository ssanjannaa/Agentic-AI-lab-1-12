"""
Application Configuration Settings
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_DB_PATH = os.path.join(DATA_DIR, "university.db")

class Settings(BaseSettings):
    APP_TITLE: str = "University Database AI Assistant"
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
    
    # Database Settings
    DATABASE_PATH: str = DEFAULT_DB_PATH
    DATABASE_READ_ONLY: bool = True
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
