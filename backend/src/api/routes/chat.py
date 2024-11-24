from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ...services.ai_assistant.llm import LLMService
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.knowledge import KnowledgeSource
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG level
llm_service = LLMService()

class ChatMessage(BaseModel):
    message: str

class Reference(BaseModel):
    url: str
    title: str
    source: str

@router.post("/")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """Process a chat message and return a response."""
    try:
        logger.debug(f"Received chat message: {message.message}")

        # First check if Ollama is available
        is_model_ready = await llm_service.check_model_status()
        if not is_model_ready:
            logger.error("Ollama model is not ready")
            return {
                "response": "I'm still initializing. Please try again in a moment.",
                "references": []
            }

        # Generate response
        logger.debug("Generating response...")
        response = await llm_service.generate_response(message.message)
        logger.debug(f"Generated response: {response[:100]}...")  # Log first 100 chars

        # Get references
        try:
            sources = db.query(KnowledgeSource).limit(3).all()
            references = [
                {
                    "url": source.url,
                    "title": source.name,
                    "source": source.type
                } for source in sources
            ]
        except Exception as e:
            logger.error(f"Error fetching references: {e}")
            references = []

        return {
            "response": response,
            "references": references
        }

    except Exception as e:
        logger.exception("Error in chat endpoint")
        return {
            "response": f"I encountered an error: {str(e)}. Please try again.",
            "references": []
        }
