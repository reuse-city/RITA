# Key Reference Files

## Docker Configuration
```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - ENVIRONMENT=development
    depends_on:
      ollama:
        condition: service_started
    command: ["./scripts/start.sh"]

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

## LLM Service Implementation
```python
# backend/src/services/ai_assistant/llm.py
class LLMService:
    def __init__(self):
        self.base_url = "http://ollama:11434"
        self.model = "orca-mini"
        
    async def generate_response(self, message: str, context: Optional[List[Dict]] = None) -> str:
        # Implementation details in current codebase
        pass
```

## Chat Route
```python
# backend/src/api/routes/chat.py
@router.post("/")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    # Implementation details in current codebase
    pass
```

## Frontend Chat Interface
```typescript
// frontend/src/components/Chat/ChatInterface.tsx
export default function ChatInterface() {
    // Implementation details in current codebase
    pass
}
```

## Directory Structure to Maintain
```
rita/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── chat.py
│   │   ├── core/
│   │   │   └── config.py
│   │   └── services/
│   │       └── ai_assistant/
│   │           └── llm.py
│   ├── scripts/
│   │   └── start.sh
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Chat/
    │   │       └── ChatInterface.tsx
    │   ├── pages/
    │   │   └── index.tsx
    │   └── styles/
    │       └── globals.css
    ├── Dockerfile
    └── package.json
```

## Essential Environment Variables
```bash
# .env
ENVIRONMENT=development
```

These files represent the core functionality of RITA. Keep them as reference when starting new development phases or branches.
