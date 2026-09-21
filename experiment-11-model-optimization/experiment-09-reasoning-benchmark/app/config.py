"""
Pydantic Settings Configuration
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    PORT: int = 8008
    HOST: str = "127.0.0.1"
    BENCHMARK_TASKS_PATH: str = "data/benchmark_tasks.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
