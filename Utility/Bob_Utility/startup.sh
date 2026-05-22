#!/bin/bash

# Azure App Service startup script for Python FastAPI application
# This script is executed when the container starts

echo "Starting Enterprise Payload Utility Toolkit..."

# Install dependencies if needed
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

# Set environment variables
export PYTHONUNBUFFERED=1
export ENVIRONMENT=${ENVIRONMENT:-production}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

# Made with Bob
