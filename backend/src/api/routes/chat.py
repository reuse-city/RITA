# backend/src/api/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatMessage(BaseModel):
    content: str
    role: str = "user"

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat endpoint that processes user messages.
    """
    try:
        # For now, just echo back the message
        return ChatResponse(
            response=f"Echo: {message.content}",
            error=None
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            response="",
            error="An error occurred processing your message"
        )
