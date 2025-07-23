#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nodejs npm docker.io docker-compose postgresql

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r ai_engine/requirements.txt
pip install -r api_service/requirements.txt
pip install -r telegram_bot/requirements.txt

# Install Node.js dependencies
cd web_ui
npm install
cd ..

# Start PostgreSQL
sudo service postgresql start

# Create database
sudo -u postgres psql -c "CREATE DATABASE soccerai;"
sudo -u postgres psql -c "CREATE USER soccerai WITH PASSWORD 'socceraipass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE soccerai TO soccerai;"

# Load schema
psql -h localhost -U soccerai -d soccerai -f database/init.sql

echo "✅ Installation complete"
echo "➡️ Run: ./scripts/start_services.sh to start the system"
