#!/bin/bash

# Load environment variables
export $(grep -v '^#' config/secrets.env | xargs)

# Start the full system
docker-compose up -d --build

# Initialize database
docker exec -it soccer-ai-db-1 psql -U user -d soccerai -f /docker-entrypoint-initdb.d/init.sql

# Start mobile emulators (Android example)
if [ "$1" == "--mobile" ]; then
  emulator -avd Pixel_6_Pro &
  adb wait-for-device
  adb install mobile_app/android/app-release.apk
fi

echo "System is running! Access:"
echo "- Web UI: http://localhost:3000"
echo "- API Docs: http://localhost:8000/docs"
