FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ai_agents/requirements.txt ./ai_agents/
COPY api_gateway/requirements.txt ./api_gateway/
COPY telegram_bot/requirements.txt ./telegram_bot/

# Install Python dependencies
RUN pip install --no-cache-dir \
    -r ai_agents/requirements.txt \
    -r api_gateway/requirements.txt \
    -r telegram_bot/requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV PRODUCTION=1

# Start services
CMD supervisord -c deployment/supervisord.conf
