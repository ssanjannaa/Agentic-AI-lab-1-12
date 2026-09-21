"""
Pydantic Settings Configuration
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    PORT: int = 8007
    HOST: str = "127.0.0.1"
    IMAGES_CATALOG_PATH: str = "data/images.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
