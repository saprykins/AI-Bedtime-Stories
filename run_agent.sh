#!/bin/bash

# Story Teller AI Agent Runner Script
# This script loads environment variables and runs the agent

# Activate virtual environment
source venv/bin/activate

# Load environment variables from .env file
if [ -f .env ]; then
    echo "🔧 Loading environment variables from .env file..."
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  No .env file found. Make sure your Azure credentials are set in environment variables."
fi

# Run the agent with all arguments passed through
echo "🎭 Starting Story Teller AI Agent..."
python story_agent.py "$@"
