#!/bin/bash

# Get the project root directory (parent of the bin directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Kill any existing processes using port 8000
echo "Checking for existing processes on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start the FastAPI server
echo "Starting FastAPI server..."
cd "$PROJECT_ROOT" && source venv/bin/activate && PYTHONPATH=$PWD python3 -m uvicorn app.main:app --reload 