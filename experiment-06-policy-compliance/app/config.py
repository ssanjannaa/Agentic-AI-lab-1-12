"""
Pydantic Settings Configuration
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    PORT: int = 8005
    HOST: str = "127.0.0.1"
    POLICIES_FILE_PATH: str = "data/policies.json"
    SCENARIOS_FILE_PATH: str = "data/scenarios.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
