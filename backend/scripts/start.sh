#!/bin/bash
set -e

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done

echo "Database is ready!"

echo "Waiting for Ollama..."
until curl -sf http://ollama:11434/api/tags > /dev/null; do
    echo "Ollama is unavailable - sleeping"
    sleep 1
done

echo "Ollama is ready! Pulling model..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "orca-mini"}'

echo "Waiting for model to be ready..."
until curl -s http://ollama:11434/api/tags | grep -q "orca-mini"; do
    echo "Model not yet available - sleeping"
    sleep 1
done

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
