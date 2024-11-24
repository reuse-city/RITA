# backend/src/core/config.py
"""
Configuration management for RITA backend.

This module manages all configuration settings, including:
- Environment variables
- Database connections
- AI model settings
- External service integrations
"""

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
    PROJECT_NAME: str = "Reuse Intelligent Technical Assistant"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI assistant for repair and reuse"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rita.db")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()