"""
Application Configuration Settings
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Agentic Cybersecurity Research & Incident Decision Assistant"
    COURSE_CODE: str = "MR23-1CS0436"
    PORT: int = 8011
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    KNOWLEDGE_BASE_DIR: str = os.path.join(DATA_DIR, "knowledge_base")
    INCIDENTS_FILE: str = os.path.join(DATA_DIR, "sample_incidents.json")
    MITRE_FILE: str = os.path.join(DATA_DIR, "mitre_mapping.json")

    # RAG Settings
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 3

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
