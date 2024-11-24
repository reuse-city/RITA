# backend/src/main.py
"""
Main application module for RITA backend.

This module initializes the FastAPI application and includes:
- API routes
- Middleware configuration
- Database initialization
- Documentation setup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning application information."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active",
        "documentation": "/docs"
    }
