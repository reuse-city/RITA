#!/bin/bash

set -e

echo "Setting up Python path..."
export PYTHONPATH="/app:${PYTHONPATH:-}"

echo "Checking required directories..."
mkdir -p src/models

# Wait for PostgreSQL
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h db -p 5432 -U postgres -d rita; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up and running!"

# Wait for Ollama
echo "Waiting for Ollama to be ready..."
until curl -s http://ollama:11434/api/tags > /dev/null; do
    echo "Ollama is unavailable - sleeping"
    sleep 1
done
echo "Ollama is up and running!"

# Initialize Alembic if needed
if [ ! -d "alembic" ]; then
    echo "Initializing Alembic..."
    alembic init alembic
    
    # Update alembic.ini with the correct database URL
    sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = postgresql://postgres:postgres@db:5432/rita|" alembic.ini
fi

# Ensure we have the correct env.py
echo "Updating Alembic environment..."
cat > alembic/env.py << 'EOL'
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Base
from src.core.config import get_settings

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOL

# Create initial migration if it doesn't exist
if [ ! "$(ls -A alembic/versions/)" ]; then
    echo "Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
