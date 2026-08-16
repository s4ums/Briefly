from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables (or a .env file
    in local development).

    Only Milestone 1 fields are declared here. See backend/.env.example for
    the full forward-looking list of variables used across all milestones —
    later milestones will add fields to this class as they introduce them
    (DATABASE_URL in M2, SUPABASE_* in M3, GROQ_API_KEY in M5/M6, etc.).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- App metadata ---
    APP_NAME: str = "Briefly API"
    ENVIRONMENT: str = "development"  # development | production
    API_V1_PREFIX: str = "/api/v1"

    # --- CORS ---
    # Comma-separated list of allowed frontend origins. Never a wildcard.
    CORS_ORIGINS: str = "http://localhost:5173"

    # --- Database (Milestone 2) ---
    # Pooled connection (PgBouncer) - used by the running app.
    DATABASE_URL: str = ""
    # Direct connection - used only by Alembic migrations, since PgBouncer
    # transaction mode can break DDL statements.
    DATABASE_URL_DIRECT: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — avoids re-parsing env vars on every request."""
    return Settings()
