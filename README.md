# Reuse Intelligent Technical Assistant (RITA)

RITA is an open-source AI assistant designed to augment repair professionals and enthusiasts, promoting reuse and circular economy principles while fostering social inclusion and environmental awareness.

## Purpose

RITA aims to:
- Augment human expertise (not replace it)
- Connect users with existing repair resources
- Promote environmental awareness and social inclusion
- Build and share repair knowledge

## Target Users

- Repair professionals
- Repair café volunteers
- Social enterprise managers
- Environmental initiatives
- Aspiring repair technicians
- Retired professionals
- Community organizers

## Key Features

- AI-powered repair assistance
- Knowledge source integration
- Community collaboration tools
- Environmental impact tracking

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/reuse-city/rita.git
cd rita
```

2. Set up the development environment:
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

3. Start the development servers:
```bash
# Start backend
cd backend
uvicorn src.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## Contributing

See [CONTRIBUTING.md](docs/community/CONTRIBUTING.md) for guidelines.

## License

GNU Affero General Public License v3.0 - see [LICENSE](LICENSE)