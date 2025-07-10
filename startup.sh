#!/bin/bash

# TradingAgents Startup Script
echo "🚀 TradingAgents Development Environment"
echo "========================================="

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment active: $(basename $VIRTUAL_ENV)"
else
    echo "❌ Virtual environment not active"
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check environment variables
if [ -f .env ]; then
    echo "✅ Environment file found"
    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
        echo "⚠️  OpenAI API key needs to be configured in .env"
    else
        echo "✅ OpenAI API key configured"
    fi
else
    echo "❌ Environment file (.env) not found"
fi

# Check dependencies
if [ -f requirements.txt ]; then
    echo "✅ Requirements file found"
else
    echo "❌ Requirements file not found"
fi

echo ""
echo "📋 Available commands:"
echo "  ta-cli    - Run CLI interface"
echo "  ta-api    - Run FastAPI server"
echo "  ta-web    - Run Streamlit web app"
echo "  ta-test   - Run tests"
echo "  ta-deps   - Install dependencies"
echo ""
echo "🎯 Ready to trade!"