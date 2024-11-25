# backend/src/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    Application settings management.
    
    Attributes:
        PROJECT_NAME: Name of the project
        VERSION: Current version
        DESCRIPTION: Project description
        DATABASE_URL: Database connection string
        ENVIRONMENT: Current environment (development/production)
    """
    PROJECT_NAME: str = "RITA"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI assistant for repair and reuse"  # This was missing
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/rita"
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
