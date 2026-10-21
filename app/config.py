"""Application settings, read from environment variables and .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Prototype uses a local SQLite file; swap to Postgres+pgvector in production
    # by setting DATABASE_URL (see .env.example).
    database_url: str = "sqlite:///./owc.db"


settings = Settings()
