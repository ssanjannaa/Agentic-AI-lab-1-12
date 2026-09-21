"""
Pydantic Settings Configuration
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    PORT: int = 8009
    HOST: str = "127.0.0.1"
    TRAIN_DATASET_PATH: str = "data/train_dataset.jsonl"
    VAL_DATASET_PATH: str = "data/val_dataset.jsonl"
    EVAL_DATASET_PATH: str = "data/eval_dataset.jsonl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
