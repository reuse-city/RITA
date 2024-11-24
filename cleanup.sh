#!/bin/bash
set -e

echo "Cleaning up RITA repository..."

# Function to ensure directory exists
ensure_dir() {
    if [ ! -d "$1" ]; then
        echo "Creating directory: $1"
        mkdir -p "$1"
    fi
}

# Function to create file if it doesn't exist
create_file() {
    if [ ! -f "$1" ]; then
        echo "Creating file: $1"
        touch "$1"
    fi
}

# Remove unnecessary directories and files
echo "Removing unnecessary files..."
rm -rf backend/alembic
rm -rf backend/src/models
rm -rf backend/src/api/routes/knowledge.py
rm -rf frontend/src/components/Knowledge
rm -rf frontend/src/types
rm -rf frontend/src/pages/knowledge

# Create necessary directory structure
echo "Creating directory structure..."
ensure_dir backend/src/api/routes
ensure_dir backend/src/core
ensure_dir backend/src/services/ai_assistant
ensure_dir backend/scripts
ensure_dir frontend/src/components/Chat
ensure_dir frontend/src/pages
ensure_dir frontend/src/styles

# Create necessary files
echo "Creating necessary files..."
create_file backend/src/__init__.py
create_file backend/src/api/__init__.py
create_file backend/src/api/routes/__init__.py
create_file backend/src/core/__init__.py
create_file backend/src/services/__init__.py
create_file backend/src/services/ai_assistant/__init__.py

# Create .gitignore
echo "Creating .gitignore..."
cat > .gitignore << 'END'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next/
out/
build/
.DS_Store
*.pem

# IDEs
.idea/
.vscode/
*.swp
*.swo

# Docker
.docker/
docker-compose.override.yml

# Project specific
ollama_data/
postgres_data/
END

echo "Clean up complete! Repository structure is now:"
tree -I 'node_modules|__pycache__|*.pyc|.git'

echo "
Next steps:
1. Review the cleaned up structure
2. Run 'docker compose down -v' to remove old volumes
3. Run 'docker compose up --build' to rebuild with clean structure"

