# Railway Configuration Guide

## Service Configuration Files

### Backend Service
- **Config File**: `railway-backend.toml`
- **Dockerfile**: `Dockerfile`
- **Port**: 8000
- **Type**: FastAPI

### Frontend Service  
- **Config File**: `railway-frontend.toml`
- **Dockerfile**: `Dockerfile.streamlit`
- **Port**: 8501
- **Type**: Streamlit

## How to Configure in Railway Dashboard

### Backend Service
1. Go to Settings → Config-as-code
2. Set Railway Config File: `railway-backend.toml`

### Frontend Service
1. Go to Settings → Config-as-code  
2. Set Railway Config File: `railway-frontend.toml`

## Environment Variables

### Backend Service
```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
FINNHUB_API_KEY=d1bkmr9r01qsbpudktsgd1bkmr9r01qsbpudktt0
DATA_DIR=./data
LLM_PROVIDER=openai
DEEP_THINK_LLM=gpt-4o
QUICK_THINK_LLM=gpt-4o
BACKEND_URL=https://api.openai.com/v1
MAX_DEBATE_ROUNDS=1
MAX_RISK_DISCUSS_ROUNDS=1
MAX_RECUR_LIMIT=100
ONLINE_TOOLS=true
```

### Frontend Service
```
BACKEND_URL=https://tradingagents-backend-production.up.railway.app
```