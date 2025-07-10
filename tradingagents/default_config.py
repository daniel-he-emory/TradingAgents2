import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "data_dir": os.getenv("DATA_DIR", "/Users/yluo/Documents/Code/ScAI/FR1-data"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
    "deep_think_llm": os.getenv("DEEP_THINK_LLM", "gpt-4o"),
    "quick_think_llm": os.getenv("QUICK_THINK_LLM", "gpt-4o"),
    "backend_url": os.getenv("BACKEND_URL", "https://api.openai.com/v1"),
    # Debate and discussion settings - minimal context
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 0,
    "max_recur_limit": 5,
    # Only market analyst is used
    "selected_analysts": ["market"],
    # Tool settings
    "online_tools": os.getenv("ONLINE_TOOLS", "true").lower() == "true",
}
