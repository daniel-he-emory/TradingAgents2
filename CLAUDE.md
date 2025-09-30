# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **consumer-friendly** multi-agent trading analysis platform for retail investors. It provides ultra-concise, visual stock analysis backed by fundamental data.

**Repository**: https://github.com/daniel-he-emory/TradingAgents2.git
**User**: daniel-he-emory (daniel.he@alumni.emory.edu)
**Status**: ✅ All tests passing (14/14), fully functional, consumer-optimized, FastAPI + Streamlit running
**Last Major Update**: 2025-09-30 - Ultra-condensed reports (50-120 words each) + enhanced visual UI

## Recent Updates (2025-09-30): Consumer-Friendly Optimization

### **Major Changes**
1. ✅ **Ultra-Condensed Reports**: All agent outputs reduced to 50-120 words (80% reduction)
2. ✅ **Investment Banker Style**: Punchy, visual, data-driven format with heavy emoji usage
3. ✅ **Enhanced UI**: Gradient headers, card layouts, color-coded metrics, two-column design
4. ✅ **More Graphics**: Required tables in every report for visual appeal
5. ✅ **Performance**: Maintained quality while drastically reducing reading time (20min → 3-5min)

### What Was Accomplished
1. ✅ Fixed all test failures (14/14 passing)
2. ✅ Installed 200+ dependencies to venv
3. ✅ Fixed FastAPI app.py to properly call `propagate()` method
4. ✅ Started FastAPI backend on http://localhost:8000
5. ✅ Verified all core dependencies working
6. ✅ Created comprehensive documentation
7. ✅ **NEW**: Optimized all agent prompts for ultra-concise output
8. ✅ **NEW**: Redesigned Streamlit UI with visual enhancements

### Critical Fixes Applied

1. **ChromaDB Singleton Conflicts** - Implemented `get_shared_chroma_client()` in `memory.py` to prevent collection conflicts across multiple `FinancialSituationMemory` instances
2. **Test Infrastructure** - Created `conftest.py` with global fixtures for ChromaDB cleanup between tests
3. **Missing Functions** - Added `create_trading_agents_graph()` factory function and `update_analysts()`/`update_debate_rounds()` helper methods to `trading_graph.py`
4. **Import Fixes** - Added `AnyMessage` import to `agent_states.py` to resolve LangGraph type hint errors
5. **Dependency Issues** - Fixed matplotlib version (3.10.0→3.5.0) for Python 3.9 compatibility, added pytest/pytest-mock
6. **Test Mocking** - Comprehensive mocking patterns in `test_trading_agents_graph.py` to prevent real API calls during testing
7. **FastAPI Bug** - Fixed `app.py` to properly call `propagate(ticker, date)` instead of passing invalid parameters

See `FIXES_APPLIED.md` and `NEXT_STEPS.md` for detailed documentation.

## Deployment

**Railway Production Deployment** (Separate Services):
- **Backend**: https://tradingagents-backend-production.up.railway.app (FastAPI, 300s timeout)
- **Frontend**: https://tradingagents-frontend-production.up.railway.app (Streamlit)

Previous deployment on Render was migrated to Railway with improved timeout handling and cross-platform compatibility.

## Environment Setup

### Prerequisites
- Python 3.9.6 (macOS system protected by PEP 668)
- OpenAI API key (required) - **Already configured in .env**
- FinnHub API key (optional, for enhanced market data)

### Dependencies Installation
**Important**: Due to macOS PEP 668 protection, dependencies are installed to `./venv/lib/python3.9/site-packages` and accessed via PYTHONPATH.

```bash
# Install dependencies (already done!)
python3 -m pip install -r requirements.txt --target ./venv/lib/python3.9/site-packages

# Set PYTHONPATH for all commands
export PYTHONPATH=./venv/lib/python3.9/site-packages
```

### Environment Variables (.env)
**Already configured** with OpenAI API key:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-... (configured)
DEEP_THINK_LLM=gpt-4o
QUICK_THINK_LLM=gpt-4o
BACKEND_URL=https://api.openai.com/v1
MAX_DEBATE_ROUNDS=1
MAX_RISK_DISCUSS_ROUNDS=1
MAX_RECUR_LIMIT=50
ONLINE_TOOLS=true
```

## Running the System

### FastAPI Backend
**Currently running on http://localhost:8000**

```bash
# Start server
export PYTHONPATH=./venv/lib/python3.9/site-packages
python3 app.py

# Or with uvicorn
uvicorn app:app --reload --port 8000
```

**API Endpoints**:
- `GET /` - API status
- `GET /health` - Health check
- `GET /trade?ticker=AAPL&date=2024-01-15` - Trading analysis

**Example**:
```bash
curl 'http://localhost:8000/trade?ticker=AAPL&date=2024-01-15'
```

### Streamlit Frontend
```bash
export PYTHONPATH=./venv/lib/python3.9/site-packages
streamlit run streamlit_app.py
```
Opens on http://localhost:8501

### Interactive CLI
```bash
export PYTHONPATH=./venv/lib/python3.9/site-packages
python3 -m cli.main
```

### Testing
```bash
# Run full test suite
export PYTHONPATH=./venv/lib/python3.9/site-packages
pytest test_trading_agents_graph.py -v

# Run specific test class
pytest test_trading_agents_graph.py::TestTradingAgentsGraph -v

# Run with detailed output
pytest test_trading_agents_graph.py -vv
```

## Architecture Overview

### Multi-Agent Workflow (LangGraph)
The system uses LangGraph to orchestrate a stateful multi-agent workflow:

1. **Analyst Team** (Parallel Analysis Phase)
   - Market Analyst: Technical indicators (MACD, RSI), price patterns
   - Fundamentals Analyst: Financial statements, company metrics
   - News Analyst: Global news, macroeconomic events
   - Social Analyst: Reddit sentiment, social media trends
   - Each analyst has dedicated tool nodes for data fetching

2. **Researcher Team** (Debate Phase)
   - Bull Researcher: Argues for investment based on analyst reports
   - Bear Researcher: Argues against investment, highlights risks
   - Research Manager: Synthesizes debate, creates investment recommendation
   - Iterates for `MAX_DEBATE_ROUNDS` with memory-enhanced arguments

3. **Trader Agent** (Decision Phase)
   - Processes investment recommendation
   - Generates initial trading plan with position sizing

4. **Risk Management Team** (Validation Phase)
   - Risky Analyst: Identifies aggressive opportunities
   - Safe Analyst: Advocates conservative approach
   - Neutral Analyst: Provides balanced perspective
   - Risk Judge: Final approval/rejection based on risk tolerance
   - Iterates for `MAX_RISK_DISCUSS_ROUNDS`

### Key Components

**`tradingagents/graph/trading_graph.py`** - Main orchestrator
- `TradingAgentsGraph`: Central class managing the workflow
- `create_trading_agents_graph()`: Factory function for instantiation
- `.propagate(ticker, date)`: Executes full analysis pipeline, returns `(final_state, processed_signal)` tuple
- Initializes LLMs, memories, toolkits, and graph structure

**`tradingagents/graph/setup.py`** - Graph construction
- `GraphSetup.setup_graph()`: Builds LangGraph StateGraph
- Creates nodes for each analyst type based on `selected_analysts`
- Connects nodes with conditional edges via `ConditionalLogic`
- Tool nodes handle data fetching with retry logic

**`tradingagents/graph/conditional_logic.py`** - Flow control
- Determines which agent speaks next in debates
- Manages debate/discussion round limits
- Routes messages to tool nodes or next agent

**`tradingagents/agents/utils/memory.py`** - ChromaDB memory
- `FinancialSituationMemory`: Stores past trading situations and outcomes
- Uses OpenAI embeddings for similarity search
- **Critical**: Uses shared ChromaDB client (`get_shared_chroma_client()`) to prevent singleton conflicts
- Supports dependency injection for testing

**`tradingagents/agents/utils/agent_states.py`** - State management
- `AgentState`: Main state passed through graph (extends `MessagesState`)
- `InvestDebateState`: Tracks bull/bear debate history
- `RiskDebateState`: Tracks risk team discussion
- **Important**: Must import `AnyMessage` from `langchain_core.messages` for type hints

**`tradingagents/agents/utils/agent_utils.py`** - Tools and utilities
- `Toolkit`: Wraps market data APIs (YFinance, FinnHub, Reddit)
- Online tools: Real-time data fetching
- Offline tools: Cached data from TradingDB

**`app.py`** - FastAPI backend
- `TradingAgentsGraph` initialized once at startup
- `/trade` endpoint calls `propagate(ticker, date)` and returns tuple `(final_state, processed_signal)`
- Response built from `final_state` dictionary keys: `final_trade_decision`, `investment_plan`, `market_report`, etc.
- **Fixed**: Properly unpacks tuple return value from `propagate()`

### Agent Initialization Pattern
All agents follow this pattern:
```python
def create_[agent_type](llm, [toolkit_or_memory]):
    system_prompt = """Role-specific instructions..."""

    def agent_node(state: AgentState):
        # Extract relevant state
        # Build prompt with context
        # Call LLM
        # Update state
        return updated_state

    return agent_node
```

## Agent Report Formats (Consumer-Optimized)

### **New Ultra-Concise Format**
All reports follow investment banker pitch style with strict word limits:

**Market Analyst** (100-120 words):
- 📊 The Story (1 sentence)
- 3 Signals with emojis
- Required data table
- Bottom line (BUY/HOLD/SELL)

**Bull/Bear Researchers** (60-80 words each):
- 1 punchy thesis sentence
- 3 catalysts/red flags (numbers only)
- 1 sentence rebuttal

**Trader** (50-70 words):
- Decision with 4-word rationale
- Trade setup table (target, horizon, confidence)
- 1 sentence action plan

**Risk Manager** (60-80 words):
- Risk level with 4-word rationale
- Risk assessment table
- Go/no-go verdict

**Key Principles**:
- Heavy emoji usage (📈📉💰🐂🐻⚠️✅🚨)
- Numbers only, no fluff
- Tables in every report
- Investment banker presentation style

## Configuration Management

### DEFAULT_CONFIG (`tradingagents/default_config.py`)
All configuration is environment-driven:
```python
DEFAULT_CONFIG = {
    "project_dir": ...,
    "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
    "deep_think_llm": os.getenv("DEEP_THINK_LLM", "gpt-4o"),
    "quick_think_llm": os.getenv("QUICK_THINK_LLM", "gpt-4o"),
    "max_debate_rounds": int(os.getenv("MAX_DEBATE_ROUNDS", "1")),
    "selected_analysts": ["market"],  # Default for cost optimization
    "online_tools": os.getenv("ONLINE_TOOLS", "true").lower() == "true",
}
```

### Token Optimization
Framework makes extensive API calls. Optimize costs:
- Use `gpt-4o-mini` for testing instead of `gpt-4o`
- Limit `selected_analysts` to `["market"]` for quick tests
- Set `MAX_DEBATE_ROUNDS=1` and `MAX_RISK_DISCUSS_ROUNDS=1`
- Use `online_tools=false` with cached data when experimenting

## Common Development Tasks

### Adding a New Analyst Type
1. Create agent in `tradingagents/agents/analysts/[type]_analyst.py`
2. Define tool functions in `Toolkit` class
3. Add tool node in `TradingAgentsGraph._create_tool_nodes()`
4. Add conditional logic in `ConditionalLogic.should_continue_[type]()`
5. Wire into graph in `GraphSetup.setup_graph()`

### Testing with Mocks
Tests use comprehensive mocking to avoid real API calls:
```python
with patch('tradingagents.graph.trading_graph.ChatOpenAI'), \
     patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
     patch('tradingagents.graph.trading_graph.Toolkit'), \
     patch('tradingagents.graph.trading_graph.set_config'):
    # Test logic here
```

Global test fixtures in `conftest.py` handle ChromaDB cleanup between tests.

### Debugging Graph Execution
```python
# Enable debug mode to see message flow
graph = TradingAgentsGraph(debug=True, config=config)
final_state, decision = graph.propagate("AAPL", "2024-01-15")

# Access state history
for key, value in final_state.items():
    print(f"{key}: {value}")
```

## Python API Usage

### Basic Usage
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Use defaults (market analyst only, optimized settings)
graph = TradingAgentsGraph()
final_state, decision = graph.propagate("AAPL", "2024-01-15")
print(f"Decision: {decision}")
print(f"Full reasoning: {final_state['final_trade_decision']}")
```

### Advanced Usage
```python
from tradingagents.graph.trading_graph import create_trading_agents_graph
from tradingagents.default_config import DEFAULT_CONFIG

# Custom configuration
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"
config["max_debate_rounds"] = 2
config["online_tools"] = True

# Select specific analysts
graph = create_trading_agents_graph(
    config=config,
    selected_analysts=["market", "fundamentals", "news"],
    debug=False
)

final_state, decision = graph.propagate("NVDA", "2024-05-10")
```

## Critical Implementation Details

### ChromaDB Singleton Issue
Always use shared client pattern to prevent collection conflicts:
```python
from tradingagents.agents.utils.memory import get_shared_chroma_client

chroma_client = get_shared_chroma_client()
memory = FinancialSituationMemory("name", config, chroma_client=chroma_client)
```

### LLM Provider Switching
Supports OpenAI, Anthropic, Google via `LLM_PROVIDER` env var:
```python
if config["llm_provider"].lower() == "openai":
    llm = ChatOpenAI(model=config["deep_think_llm"], base_url=config["backend_url"])
elif config["llm_provider"].lower() == "anthropic":
    llm = ChatAnthropic(model=config["deep_think_llm"], base_url=config["backend_url"])
elif config["llm_provider"].lower() == "google":
    llm = ChatGoogleGenerativeAI(model=config["deep_think_llm"])
```

### State Propagation
State flows through graph immutably - each agent returns updated state:
```python
def agent_node(state: AgentState):
    return {
        **state,  # Preserve existing state
        "market_report": new_report,  # Update specific fields
        "messages": state["messages"] + [new_message],
    }
```

### FastAPI propagate() Return Value
**Important**: `propagate()` returns a tuple `(final_state, processed_signal)`:
```python
final_state, processed_signal = ta.propagate(ticker, date)

# Extract data from final_state dict
recommendation = final_state["final_trade_decision"]
market_report = final_state["market_report"]
# etc.
```

## Research vs Production

**This is a research framework, not production trading software:**
- No real order execution or broker integration
- Results vary with LLM model, temperature, data quality
- Intended for research, education, and experimentation
- See disclaimer: https://tauric.ai/disclaimer/

## Project Constraints & Best Practices

### Testing Philosophy
- **Isolated unit tests** with comprehensive mocking over integration tests
- Mock all external dependencies (ChatOpenAI, FinancialSituationMemory, Toolkit, etc.)
- Use context managers for mocking, not decorators
- Tests must pass without real API calls

### ChromaDB Management
- Always use shared client instance via `get_shared_chroma_client()`
- Proper cleanup happens automatically via `conftest.py`
- Never create multiple ChromaDB clients
- Support dependency injection for testing

### Code Safety
- Never share API keys in code or commit history
- `.env` file is in `.gitignore` - keep it that way
- Use environment variables for all configuration

### Python Environment
- **Python 3.9.6** on macOS (system protected by PEP 668)
- **Always set PYTHONPATH**: `export PYTHONPATH=./venv/lib/python3.9/site-packages`
- Never use `--break-system-packages` flag
- Install all packages with `--target ./venv/lib/python3.9/site-packages`

### LLM Configuration
- Default: OpenAI with gpt-4o for both deep and quick thinking
- Token optimization: MAX_DEBATE_ROUNDS=1, MAX_RISK_DISCUSS_ROUNDS=1, MAX_RECUR_LIMIT=50
- For testing: Use gpt-4o-mini to save costs
- Framework makes **many** API calls - be cost-conscious

## Troubleshooting

### Import Errors
- Set PYTHONPATH: `export PYTHONPATH=./venv/lib/python3.9/site-packages`
- Check Python version: `python3 --version` (need 3.9+)
- Reinstall dependencies: `python3 -m pip install -r requirements.txt --target ./venv/lib/python3.9/site-packages`

### ChromaDB Collection Errors
- Tests automatically cleanup via `conftest.py` fixtures
- Manual cleanup: Delete `tradingagents/dataflows/data_cache/chroma.sqlite3`

### API Rate Limits
- Use cheaper models for testing (`gpt-4o-mini`)
- Reduce debate rounds and analyst count
- Enable caching with `online_tools=false`

### macOS System Python Protection
- Always set PYTHONPATH before running any command
- Don't use `--break-system-packages`
- Install to venv/lib/python3.9/site-packages with --target flag

### Test Failures
- Verify conftest.py exists and has ChromaDB cleanup fixtures
- Check that all mocks are properly configured in test files
- Ensure AnyMessage is imported in agent_states.py
- Run with `-vv` flag for detailed output

### FastAPI propagate() Errors
- Remember: `propagate()` only takes `(ticker, date)` parameters
- Returns tuple: `(final_state, processed_signal)`
- Extract data from `final_state` dictionary
- Model/round configuration must be done at graph initialization

## Citation

When using this framework in research:
```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
  title={TradingAgents: Multi-Agents LLM Financial Trading Framework},
  author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
  year={2025},
  eprint={2412.20138},
  archivePrefix={arXiv},
  primaryClass={q-fin.TR},
  url={https://arxiv.org/abs/2412.20138}
}
```