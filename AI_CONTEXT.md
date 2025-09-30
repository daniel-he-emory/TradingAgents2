# AI Collaboration Protocol

## Role-Based AI Interaction

- **Gemini (Architect)**: Project architect - analyzes codebase, identifies issues, designs solutions
- **Claude (Builder)**: Project builder - executes prompts by writing, debugging, and modifying code

---

# Previous Work Summary

## Railway Deployment (Completed)
Successfully migrated TradingAgents from Render to Railway with separate backend and frontend services:
- **Backend**: `https://tradingagents-backend-production.up.railway.app` (FastAPI, 300s timeout)
- **Frontend**: `https://tradingagents-frontend-production.up.railway.app` (Streamlit)
- **Framework Update**: Updated to latest upstream TradingAgents with improved AI support
- **Key Fixes**: ChromaDB conflicts, package imports, timeout issues, cross-platform compatibility

## Previous Session - Test Infrastructure Fixes
- Implemented ChromaDB dependency injection pattern
- Created conftest.py for global pytest fixtures
- Fixed test mocking strategies with context managers
- Achieved passing test suite through architectural refactoring

---

# Current Session Context

## Objective
Complete end-to-end fix of TradingAgents2 framework issues, verify all functionality with real API, and document setup for running the web app, CLI, and trading analysis.

## Key Files
* `/Users/danielhe/TradingAgents2/.env` - Environment configuration with OpenAI API key
* `/Users/danielhe/TradingAgents2/conftest.py` - Global pytest fixtures for ChromaDB cleanup
* `/Users/danielhe/TradingAgents2/tradingagents/agents/utils/memory.py` - Shared ChromaDB client implementation
* `/Users/danielhe/TradingAgents2/tradingagents/agents/utils/agent_states.py` - Fixed AnyMessage import
* `/Users/danielhe/TradingAgents2/tradingagents/graph/trading_graph.py` - Added factory function and helper methods
* `/Users/danielhe/TradingAgents2/test_trading_agents_graph.py` - Fixed all test mocking issues
* `/Users/danielhe/TradingAgents2/requirements.txt` - Added pytest, fixed matplotlib version
* `/Users/danielhe/TradingAgents2/FIXES_APPLIED.md` - Complete documentation of all fixes
* `/Users/danielhe/TradingAgents2/NEXT_STEPS.md` - User guide for running applications

## Key Decisions
* **ChromaDB Singleton Fix**: Implemented `get_shared_chroma_client()` function with global client instance to prevent conflicts
* **Test Infrastructure**: Created comprehensive conftest.py with automatic ChromaDB cleanup between tests
* **Missing Functions**: Added `create_trading_agents_graph()` factory function and `update_analysts()`/`update_debate_rounds()` helper methods
* **Import Fixes**: Added `AnyMessage` import to agent_states.py to resolve LangGraph type hint errors
* **Environment Setup**: Created `.env` file with user's OpenAI API key (configured)
* **Dependency Management**: Fixed matplotlib version (3.10.0→3.5.0) for Python 3.9 compatibility
* **Test Mocking**: Comprehensive mocking of all external dependencies (ChatOpenAI, FinancialSituationMemory, Toolkit, etc.)
* **macOS Python Protection**: Documented workaround for PEP 668 system Python protection using venv

## Current Status
**✅ ALL FIXES COMPLETED - 14/14 tests passing**

Successfully fixed all test failures and architectural issues:
1. ✅ Created `.env` with OpenAI API key
2. ✅ Fixed ChromaDB singleton conflicts with shared client pattern
3. ✅ Added pytest and pytest-mock to requirements.txt
4. ✅ Fixed matplotlib version incompatibility
5. ✅ Created conftest.py with global test fixtures
6. ✅ Fixed all mocking issues in test files
7. ✅ Added missing `create_trading_agents_graph()` factory function
8. ✅ Added `AnyMessage` import to fix LangGraph type hints
9. ✅ Created comprehensive documentation (FIXES_APPLIED.md, NEXT_STEPS.md)

**Next Steps**: User needs to activate venv and install dependencies to run apps:
```bash
source venv/bin/activate
pip install -r requirements.txt
python app.py  # or streamlit run streamlit_app.py, or python -m cli.main
```

## Constraints & Preferences
* **User Identity**: GitHub username is `daniel-he-emory`, email is `daniel.he@alumni.emory.edu`
* **Repository**: `https://github.com/daniel-he-emory/TradingAgents2.git`
* **Working Directory**: `/Users/danielhe/TradingAgents2`
* **Python Version**: Python 3.9.6 (macOS system protected by PEP 668)
* **Testing Philosophy**: Isolated unit tests with comprehensive mocking
* **ChromaDB Management**: Shared client instance with proper cleanup
* **API Keys**: OpenAI API key configured in `.env`, never share in chat
* **Virtual Environment**: Use `venv/` for package installation due to system Python protection
* **LLM Provider**: OpenAI (gpt-4o for both deep and quick thinking)
* **Token Optimization**: MAX_DEBATE_ROUNDS=1, MAX_RISK_DISCUSS_ROUNDS=1, MAX_RECUR_LIMIT=50