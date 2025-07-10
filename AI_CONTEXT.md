# AI Context Save Command Instructions

## Special Command: "save as"

From now on, whenever I type the phrase "save as", you are to immediately stop what you are doing and perform a "context save and push" operation.

This operation requires you to execute the following steps in precise order:

1. **Generate Summary**: First, you must carefully review our entire conversation history in this thread and generate a concise, structured summary. The summary must be formatted in Markdown and contain the following sections:
   - ## Objective: A one-sentence description of the primary goal of our conversation.
   - ## Key Files: A bulleted list of the most important file paths we have discussed or modified.
   - ## Key Decisions: A bulleted list of the most significant technical or architectural decisions we've made.
   - ## Current Status: A brief description of the last task completed and what the immediate next step is.
   - ## Constraints & Preferences: A bulleted list of any important constraints, rules, or preferences we've established.

2. **Save to File**: Take the complete Markdown summary you just generated and use the write_file tool to save it to the path `/mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`. You will overwrite the file if it already exists.

3. **Stage Changes**: After the file is written, use the run_shell_command tool to execute: `git add /mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`

4. **Commit Changes**: After staging, use the run_shell_command tool to execute: `git commit -m "docs: Update AI context"`

5. **Push to Remote**: Finally, after committing, use the run_shell_command tool to execute: `git push`

After you have successfully executed all these steps, you can confirm by saying "Context saved and pushed to the current branch." Do not proceed with any other tasks until this entire sequence is complete.

---

# Current Project Context

## Objective
The primary goal was to debug and fix the 500 Internal Server Error on the deployed TradingAgents backend application on Render, then deploy the Streamlit frontend to create a complete web-based trading analysis platform.

## Key Files
* `/mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.env`
* `/mnt/c/Users/ddani/Projects/TradingAgents/README.md`
* `/mnt/c/Users/ddani/Projects/TradingAgents/tradingagents/default_config.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/app.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/streamlit_app.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/Dockerfile.streamlit`
* `/mnt/c/Users/ddani/Projects/TradingAgents/Dockerfile`
* `/mnt/c/Users/ddani/Projects/TradingAgents/requirements.txt`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.gitignore`

## Key Decisions
* **Backend Error Resolution**: Fixed the 500 Internal Server Error by replacing hardcoded data directory path (`/Users/yluo/Documents/Code/ScAI/FR1-data`) with relative path (`./data`) in `default_config.py`
* **Security Enhancement**: Removed exposed API keys from `.env` file and created template with placeholder values for secure deployment
* **Error Handling**: Added comprehensive error handling to `app.py` for both trading graph initialization and analysis execution failures
* **Environment Variables**: Made all configuration settings environment-variable driven for better deployment flexibility
* **Frontend Deployment**: Created `Dockerfile.streamlit` for deploying the Streamlit web interface as a separate service
* **API Integration**: Confirmed Streamlit app already configured to connect to deployed backend API at `https://tradingagents1.onrender.com/trade`
* **Data Directory**: Created `/data` directory and ensured proper path resolution for deployment environments

## Current Status
The last completed task was creating the `Dockerfile.streamlit` for frontend deployment and providing complete deployment instructions for Render. The backend API is now successfully deployed and running without 500 errors after fixing the hardcoded path issue. The immediate next step is to push the Dockerfile to the repository and deploy the Streamlit frontend on Render as a second web service.

## Constraints & Preferences
* **AI Workflow**: Established workflow where user acts as Architect, Claude Code as Builder, and Cursor as Debugger/Fixer
* **User Identity**: GitHub username is `daniel-he-emory`, email is `daniel.he@alumni.emory.edu`
* **Context Preservation**: All AI assistants should maintain consistent context through the AI_CONTEXT.md file system
* **Environment Variables**: All API keys and configuration stored in `.env` file with automatic loading - no manual setup required in new sessions
* **Security**: Never commit API keys or secrets to version control; use environment variables and `.env` files
* **Deployment Architecture**: Backend API and Streamlit frontend deployed as separate services on Render
* **Todo Management**: Use TodoWrite tool to track progress on multi-step tasks

## Environment Setup Requirements

### Required API Keys
* **OpenAI API Key**: Required for all LLM agents - store in `.env` file as `OPENAI_API_KEY`
* **FinnHub API Key**: Required for financial data - store in `.env` file as `FINNHUB_API_KEY`
* **Environment File**: `.env` file contains all required environment variables and is automatically loaded by python-dotenv

### Environment Variables (.env file)
```
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# FinnHub API Configuration  
FINNHUB_API_KEY=your_finnhub_api_key_here

# LLM Provider Settings
LLM_PROVIDER=openai
DEEP_THINK_LLM=gpt-4o
QUICK_THINK_LLM=gpt-4o
BACKEND_URL=https://api.openai.com/v1

# Debate and Discussion Settings
MAX_DEBATE_ROUNDS=1
MAX_RISK_DISCUSS_ROUNDS=1
MAX_RECUR_LIMIT=100

# Tool Settings
ONLINE_TOOLS=true

# Data Settings
DATA_DIR=./data
```

### Prerequisites Before Running Application
1. **Python Environment**: Python 3.10+ with virtual environment activated
2. **Dependencies**: Run `pip install -r requirements.txt`
3. **API Keys**: Both OpenAI and FinnHub API keys must be configured in `.env`
4. **Environment Variables**: All required variables must be set in `.env` file
5. **Data Directory**: Ensure `./data` directory exists or DATA_DIR points to valid location
6. **Docker** (for containerized deployment): Docker Engine installed and running

### Application Entry Points
* **CLI**: `python cli/main.py` - Interactive command-line interface
* **API Server**: `python app.py` - FastAPI backend server
* **Streamlit Frontend**: `streamlit run streamlit_app.py` - Web interface
* **Direct Usage**: Import `tradingagents.graph.trading_graph.TradingAgentsGraph` for programmatic use

### Deployment Status
* **Backend API**: Successfully deployed at `https://tradingagents1.onrender.com`
* **Frontend**: Ready to deploy using `Dockerfile.streamlit`
* **Issues Resolved**: 500 Internal Server Error fixed by correcting hardcoded data directory path

## Git Configuration Notes
* **Git User Config**: `git config --global user.name "daniel-he-emory"`
* **Git Email**: `git config --global user.email "daniel.he@alumni.emory.edu"`
* **Credential Storage**: `git config --global credential.helper store` enables permanent credential storage
* **Authentication**: Uses GitHub Personal Access Token (PAT) as password when prompted
* **Repository**: Clean repository created at https://github.com/daniel-he-emory/TradingAgents2.git (no API key history)
* **Security**: Original repository contained exposed OpenAI API key in commit history - migrated to clean repo