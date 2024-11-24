from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    """Application settings."""
    PROJECT_NAME: str = "Reuse Intelligent Technical Assistant"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/rita"
    )
    
    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
