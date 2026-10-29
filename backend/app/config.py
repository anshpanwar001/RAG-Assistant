"""
Application settings, loaded from environment variables.

Keeping configuration out of the code means the same code can run on your
laptop (with a .env file) and in production (with real environment variables)
without any changes.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root: backend/app/config.py -> backend/app -> backend -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Typed settings. Pydantic checks each value's type when the app starts."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    data_dir: Path = PROJECT_ROOT / "data"


@lru_cache
def get_settings() -> Settings:
    """
    Return one shared Settings object.

    lru_cache means the .env file is read once, not on every request.
    """
    return Settings()