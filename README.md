# Reuse Intelligent Technical Assistant (RITA)

RITA is an AI-powered assistant designed to support repair professionals and communities in promoting reuse and circular economy practices.

## Current Status
- Basic chat interface implemented
- Integration with Ollama using Orca-mini model
- Focuses on repair and reuse guidance

## Architecture

### Backend (FastAPI)
- Location: `/backend`
- Key Components:
  - Chat Service (`/src/services/ai_assistant/llm.py`)
  - API Routes (`/src/api/routes/chat.py`)
  - Configuration (`/src/core/config.py`)

### Frontend (Next.js)
- Location: `/frontend`
- Key Components:
  - Chat Interface (`/src/components/Chat/ChatInterface.tsx`)
  - Main Page (`/src/pages/index.tsx`)

### Infrastructure
- Docker-based deployment
- Uses Ollama for local LLM hosting
- Orca-mini model (chosen for lower memory requirements)

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Git
- 4GB+ available memory

### Quick Start
```bash
# Clone repository
git clone https://github.com/reuse-city/rita.git
cd rita

# Start services
docker compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Key Decisions
1. **LLM Choice**: Using Orca-mini instead of larger models due to memory constraints
2. **Architecture**: Microservices architecture with Docker for easy deployment
3. **Focus**: Emphasizing repair knowledge and sustainability in AI responses

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
GNU Affero General Public License v3.0

## Project Vision
RITA aims to augment (not replace) human expertise in repair and reuse, promoting sustainable practices and knowledge sharing within the repair community.
