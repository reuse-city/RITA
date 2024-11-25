# backend/src/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from .core.config import get_settings
from contextlib import asynccontextmanager
from .api.routes import chat  # Import the chat router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application...")
    try:
        pass
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
    yield
    logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint returning application information."""
    try:
        return {
            "project": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "active",
            "documentation": "/docs"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Error handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
