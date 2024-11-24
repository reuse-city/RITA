import httpx
import json
import logging
from typing import Dict, List, Optional
from ...core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class LLMService:
    def __init__(self):
        self.base_url = "http://ollama:11434"
        self.model = "orca-mini"  # Changed to a smaller model
        logger.info(f"Initialized LLMService with base_url: {self.base_url}")
        
    async def check_model_status(self) -> bool:
        """
        Check if the required model is available.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    logger.error("Failed to get model tags")
                    return False
                    
                data = response.json()
                models = data.get("models", [])
                logger.info(f"Available models: {models}")
                
                # Check if our model is in the list
                model_available = any(model.get("name") == self.model for model in models)
                logger.info(f"Model {self.model} available: {model_available}")
                return model_available
                
        except Exception as e:
            logger.error(f"Error checking model status: {str(e)}")
            return False
        
    async def generate_response(self, 
                              message: str, 
                              context: Optional[List[Dict]] = None) -> str:
        """
        Generate a response using Ollama.
        """
        try:
            # Check if model is ready
            if not await self.check_model_status():
                logger.warning("Model not ready, attempting to pull...")
                try:
                    async with httpx.AsyncClient() as client:
                        await client.post(f"{self.base_url}/api/pull", json={"name": self.model})
                    logger.info("Model pull initiated")
                except Exception as e:
                    logger.error(f"Error pulling model: {str(e)}")
                return "I'm still initializing my language model. Please try again in a moment."

            prompt = self._create_prompt(message, context)
            logger.info(f"Sending request to Ollama with prompt: {prompt[:100]}...")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info("Making request to Ollama...")
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                logger.info(f"Received response status: {response.status_code}")
                
                if response.status_code != 200:
                    logger.error(f"Ollama error: {response.text}")
                    return "I'm having trouble processing your request. Please try again."
                
                result = response.json()
                response_text = result.get('response', '')
                logger.info(f"Processed response: {response_text[:100]}...")
                return response_text
                
        except httpx.TimeoutException:
            logger.error("Request to Ollama timed out")
            return "I'm taking too long to respond. Please try again."
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I encountered an error while processing your request. Please try again."
    
    def _create_prompt(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """
        Create a prompt that emphasizes RITA's focus on repair, reuse, and sustainability.
        """
        base_prompt = """You are RITA (Reuse Intelligent Technical Assistant), an AI designed to:
- Help users with repair and maintenance guidance
- Promote reuse and sustainable practices
- Connect users with repair resources and communities
- Share knowledge while giving credit to sources

Remember to:
- Prioritize repair and reuse over replacement
- Consider environmental impact
- Reference existing repair resources when possible
- Be clear about safety considerations
- Acknowledge when expert help is needed

User's message: {message}"""

        return base_prompt.format(message=message)
