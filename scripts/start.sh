#!/bin/bash

# Start database
docker-compose -f database/docker-compose-db.yml up -d

# Start AI engine
cd ai_engine && python main.py &

# Start API service
cd api_service && python app.py &

# Start Telegram bot
cd telegram_bot && python bot.py &

# Start web UI
cd web_ui && npm start &

echo "✅ All services started successfully!"
echo "🌐 Web UI: http://localhost:3000"
echo "📱 API: http://localhost:8000"
