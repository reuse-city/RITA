from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import chat, knowledge
from .core.config import get_settings
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI assistant for repair and reuse",
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

# Include routers
app.include_router(
    chat.router,
    prefix="/api/v1/chat",
    tags=["chat"]
)

app.include_router(
    knowledge.router,
    prefix="/api/v1/knowledge",
    tags=["knowledge"]
)

@app.get("/")
async def root():
    """Root endpoint returning application information."""
    return {
        "status": "online",
        "version": settings.VERSION
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        # Check Ollama connection
        is_model_ready = await app.state.llm_service.check_model_status()
        return {
            "status": "healthy",
            "ollama_status": "ready" if is_model_ready else "not ready"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
