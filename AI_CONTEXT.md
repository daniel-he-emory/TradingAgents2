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
The primary goal was to create a fully automated, zero-friction development environment for the TradingAgents multi-agent framework with persistent configuration, automatic startup, and comprehensive AI assistant context preservation.

## Key Files
* `/mnt/c/Users/ddani/Projects/TradingAgents/AI_CONTEXT.md`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.env`
* `/mnt/c/Users/ddani/Projects/TradingAgents/README.md`
* `/mnt/c/Users/ddani/Projects/TradingAgents/startup.sh`
* `~/.bashrc` (shell configuration with automation)
* `/mnt/c/Users/ddani/Projects/TradingAgents/docker-compose.yml`
* `/mnt/c/Users/ddani/Projects/TradingAgents/Dockerfile` (for the API service)
* `/mnt/c/Users/ddani/Projects/TradingAgents/requirements.txt`
* `/mnt/c/Users/ddani/Projects/TradingAgents/requirements.in`
* `/mnt/c/Users/ddani/Projects/TradingAgents/streamlit_app.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/app.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/cli/main.py`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.dockerignore`
* `/mnt/c/Users/ddani/Projects/TradingAgents/.gitignore`

## Key Decisions
* **Context Management System**: Established a "save as" command that generates structured summaries and commits them to version control for consistency across AI assistants.
* **Security Migration**: Created a new clean GitHub repository (TradingAgents2.git) after discovering exposed OpenAI API key in commit history.
* **Environment Variables**: Configured secure storage of API keys in `.env` file with automatic loading via python-dotenv - no manual key entry required in new sessions.
* **Complete API Configuration**: Set up both OpenAI and FinnHub API keys in `.env` file for persistent access.
* **Full Shell Automation**: Configured ~/.bashrc for automatic virtual environment activation, project directory navigation, and startup script execution.
* **Command Aliases**: Created convenient shortcuts (ta-cli, ta-api, ta-web, ta-test, ta-deps, ta-status, ta-push) for common operations.
* **Startup Health Check**: Implemented startup.sh script that validates environment configuration and displays available commands.
* **Documentation Enhancement**: Updated README.md to direct AI assistants to read AI_CONTEXT.md first for project understanding.
* **Git Configuration**: Fully configured Git with user credentials, email, and credential helper for persistent authentication.
* **Comprehensive Setup Documentation**: Added detailed environment setup requirements, prerequisites, and application entry points to AI_CONTEXT.md.
* **Previous TradingAgents Decisions**: Native Docker Engine in WSL2, microservices architecture, Render for backend hosting, pip-tools for dependency management, and Gunicorn for production.

## Current Status
The last completed task was implementing comprehensive shell automation including auto-activation of virtual environment, automatic project directory navigation, command aliases, and startup health checking. The development environment is now completely zero-friction - opening a new terminal automatically sets up the entire development context. The application is ready to run with all required configurations in place. The immediate next step is to debug the 500 Internal Server Error occurring on the deployed backend application on Render.

## Constraints & Preferences
* **AI Workflow**: Established workflow where user acts as Architect, Claude Code as Builder, and Cursor as Debugger/Fixer.
* **User Identity**: GitHub username is `daniel-he-emory`, email is `daniel.he@alumni.emory.edu`.
* **Context Preservation**: All AI assistants should maintain consistent context through the AI_CONTEXT.md file system.
* **Environment Variables**: All API keys and configuration stored in `.env` file with automatic loading - no manual setup required in new sessions.
* **Security**: Never commit API keys or secrets to version control; use environment variables and `.env` files.
* **Zero-Friction Development**: Setup is designed to be completely automated with no manual steps required in new sessions.
* **Command Shortcuts**: Use aliases (ta-cli, ta-api, ta-web, etc.) for quick access to common operations.

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
FINNHUB_API_KEY=d1bkmr9r01qsbpudktsgd1bkmr9r01qsbpudktt0

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
1. **Python Environment**: Python 3.10+ with virtual environment activated (automated)
2. **Dependencies**: Run `pip install -r requirements.txt` or use alias `ta-deps`
3. **API Keys**: Both OpenAI and FinnHub API keys must be configured in `.env`
4. **Environment Variables**: All required variables must be set in `.env` file
5. **Data Directory**: Ensure `./data` directory exists or DATA_DIR points to valid location
6. **Docker** (for containerized deployment): Docker Engine installed and running

### Application Entry Points & Aliases
* **CLI**: `ta-cli` or `python cli/main.py` - Interactive command-line interface
* **API Server**: `ta-api` or `python app.py` - FastAPI backend server
* **Streamlit Frontend**: `ta-web` or `streamlit run streamlit_app.py` - Web interface
* **Tests**: `ta-test` or `python test_trading_agents_graph.py` - Run test suite
* **Dependencies**: `ta-deps` or `pip install -r requirements.txt` - Install dependencies
* **Git Status**: `ta-status` or `git status` - Check repository status
* **Quick Push**: `ta-push` - Add, commit, and push changes
* **Direct Usage**: Import `tradingagents.graph.trading_graph.TradingAgentsGraph` for programmatic use

### Automated Shell Configuration
* **Virtual Environment**: Automatically activated on terminal startup
* **Project Directory**: Automatically navigated to on terminal startup
* **Startup Health Check**: Automatically runs startup.sh to validate environment
* **Command Aliases**: All shortcuts automatically available
* **No Manual Setup**: Zero manual steps required for new sessions

## Git Configuration Notes
* **Git User Config**: `git config --global user.name "daniel-he-emory"`
* **Git Email**: `git config --global user.email "daniel.he@alumni.emory.edu"`
* **Credential Storage**: `git config --global credential.helper store` enables permanent credential storage
* **Authentication**: Uses GitHub Personal Access Token (PAT) as password when prompted
* **Repository**: Clean repository created at https://github.com/daniel-he-emory/TradingAgents2.git (no API key history)
* **Security**: Original repository contained exposed OpenAI API key in commit history - migrated to clean repo