FROM python:3.9

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the start script first and make it executable
COPY scripts/start.sh /app/scripts/start.sh
RUN chmod +x /app/scripts/start.sh

# Copy the rest of the application
COPY . .

# Make sure the script is still executable after copying everything
RUN chmod +x /app/scripts/start.sh

# Use bash to run the script
CMD ["bash", "/app/scripts/start.sh"]
