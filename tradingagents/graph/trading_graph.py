import os
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.memory import FinancialSituationMemory
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.dataflows.interface import set_config

from .setup import GraphSetup
from .conditional_logic import ConditionalLogic
from .propagation import Propagator


class TradingAgentsGraph:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or DEFAULT_CONFIG.copy()
        # Always use only the market analyst
        self.selected_analysts = ["market"]
        # Set minimal context config
        self.config["max_debate_rounds"] = 1
        self.config["max_risk_discuss_rounds"] = 0
        self.config["max_recur_limit"] = 5
        self.config["selected_analysts"] = ["market"]
        set_config(self.config)
        os.makedirs(
            os.path.join(self.config["project_dir"], "dataflows/data_cache"),
            exist_ok=True,
        )
        # Always disable function calling for OpenAI/Anthropic
        if self.config["llm_provider"].lower() in ("openai", "ollama", "openrouter"):
            self.deep_thinking_llm = ChatOpenAI(model=self.config["deep_think_llm"], base_url=self.config["backend_url"], api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"tools": []})
            self.quick_thinking_llm = ChatOpenAI(model=self.config["quick_think_llm"], base_url=self.config["backend_url"], api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"tools": []})
        elif self.config["llm_provider"].lower() == "anthropic":
            self.deep_thinking_llm = ChatAnthropic(model=self.config["deep_think_llm"], base_url=self.config["backend_url"], model_kwargs={"tools": []})
            self.quick_thinking_llm = ChatAnthropic(model=self.config["quick_think_llm"], base_url=self.config["backend_url"], model_kwargs={"tools": []})
        elif self.config["llm_provider"].lower() == "google":
            self.deep_thinking_llm = ChatGoogleGenerativeAI(model=self.config["deep_think_llm"])
            self.quick_thinking_llm = ChatGoogleGenerativeAI(model=self.config["quick_think_llm"])
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config['llm_provider']}")
        self.toolkit = Toolkit(config=self.config)
        self.bull_memory = FinancialSituationMemory("bull_memory", self.config)
        self.bear_memory = FinancialSituationMemory("bear_memory", self.config)
        self.trader_memory = FinancialSituationMemory("trader_memory", self.config)
        self.invest_judge_memory = FinancialSituationMemory("invest_judge_memory", self.config)
        self.risk_manager_memory = FinancialSituationMemory("risk_manager_memory", self.config)
        self.tool_nodes = {
            "market": ToolNode([
                self.toolkit.get_YFin_data_online,
                self.toolkit.get_stockstats_indicators_report_online,
                self.toolkit.get_YFin_data,
                self.toolkit.get_stockstats_indicators_report,
            ]),
        }
        self.conditional_logic = ConditionalLogic(
            max_debate_rounds=1,
            max_risk_discuss_rounds=0
        )
        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            self.toolkit,
            self.tool_nodes,
            self.bull_memory,
            self.bear_memory,
            self.trader_memory,
            self.invest_judge_memory,
            self.risk_manager_memory,
            self.conditional_logic,
        )
        self.propagator = Propagator(
            max_recur_limit=5
        )
        self.compiled_graph = self.graph_setup.setup_graph(self.selected_analysts)

    def propagate(
        self,
        company_name: str,
        trade_date: str,
        deep_think_model: Optional[str] = None,
        quick_think_model: Optional[str] = None,
        debate_rounds: Optional[int] = None,
    ) -> Dict[str, Any]:
        # Per-request LLM/model override
        if deep_think_model:
            if self.config["llm_provider"].lower() in ("openai", "ollama", "openrouter"):
                self.deep_thinking_llm = ChatOpenAI(model=deep_think_model, base_url=self.config["backend_url"], api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"tools": []})
            elif self.config["llm_provider"].lower() == "anthropic":
                self.deep_thinking_llm = ChatAnthropic(model=deep_think_model, base_url=self.config["backend_url"], model_kwargs={"tools": []})
            elif self.config["llm_provider"].lower() == "google":
                self.deep_thinking_llm = ChatGoogleGenerativeAI(model=deep_think_model)
        
        if quick_think_model:
            if self.config["llm_provider"].lower() in ("openai", "ollama", "openrouter"):
                self.quick_thinking_llm = ChatOpenAI(model=quick_think_model, base_url=self.config["backend_url"], api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"tools": []})
            elif self.config["llm_provider"].lower() == "anthropic":
                self.quick_thinking_llm = ChatAnthropic(model=quick_think_model, base_url=self.config["backend_url"], model_kwargs={"tools": []})
            elif self.config["llm_provider"].lower() == "google":
                self.quick_thinking_llm = ChatGoogleGenerativeAI(model=quick_think_model)
        if debate_rounds is not None:
            self.conditional_logic.max_debate_rounds = debate_rounds
        # Clear all memories before each run to minimize context
        for mem in [self.bull_memory, self.bear_memory, self.trader_memory, self.invest_judge_memory, self.risk_manager_memory]:
            if hasattr(mem, 'situation_collection'):
                try:
                    # Get all document IDs first
                    all_docs = mem.situation_collection.get()
                    if all_docs['ids']:
                        mem.situation_collection.delete(ids=all_docs['ids'])
                except Exception:
                    # If deletion fails, continue without clearing
                    pass
        initial_state = self.propagator.create_initial_state(company_name, trade_date)
        graph_args = self.propagator.get_graph_args()
        result = self.compiled_graph.invoke(initial_state, graph_args)
        # Extract extended data for API response
        extended_result = self._extract_extended_data(result)
        return extended_result

    def _extract_extended_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract extended data from the graph execution result."""
        # Extract analyst reports
        analyst_reports = {
            "market_report": result.get("market_report", ""),
            "news_report": result.get("news_report", ""),
            "sentiment_report": result.get("sentiment_report", ""),
            "technical_report": result.get("fundamentals_report", "")  # Map fundamentals to technical
        }
        
        # Extract debate logs
        investment_debate = result.get("investment_debate_state", {})
        debate_logs = []
        
        # Extract bull and bear history if available
        bull_history = investment_debate.get("bull_history", "")
        bear_history = investment_debate.get("bear_history", "")
        general_history = investment_debate.get("history", "")
        
        if bull_history:
            debate_logs.append({"round": 1, "type": "bull", "message": bull_history})
        if bear_history:
            debate_logs.append({"round": 1, "type": "bear", "message": bear_history})
        if general_history and not bull_history and not bear_history:
            # Parse general history into rounds if structured
            debate_logs.append({"round": 1, "type": "general", "message": general_history})
        
        # Extract risk management data
        risk_debate = result.get("risk_debate_state", {})
        risk_management = {
            "risky_summary": risk_debate.get("current_risky_response", ""),
            "safe_summary": risk_debate.get("current_safe_response", ""),
            "neutral_summary": risk_debate.get("current_neutral_response", ""),
            "judge_decision": risk_debate.get("judge_decision", ""),
            "final_recommendation": result.get("final_trade_decision", "")
        }
        
        # Extract basic trading data for backward compatibility
        final_decision = result.get("final_trade_decision", "")
        processed_signal = self.process_signal(final_decision)
        
        return {
            # Original fields for backward compatibility
            "final_trade_decision": final_decision,
            "recommendation": processed_signal,
            "reasoning": final_decision,
            "processed_signal": processed_signal,
            "confidence": "High" if any(word in final_decision.lower() for word in ["strong", "confident", "high"]) else "Medium",
            
            # Extended fields
            "analyst_reports": analyst_reports,
            "debate_logs": debate_logs,
            "risk_management": risk_management,
            
            # Individual risk summaries for UI compatibility
            "risky_summary": risk_management.get("risky_summary", ""),
            "safe_summary": risk_management.get("safe_summary", ""),
            "neutral_summary": risk_management.get("neutral_summary", ""),
        }

    # Backward compatibility methods
    def process_signal(self, full_signal: str) -> str:
        """Process trading signals to extract decisions (backward compatibility)."""
        # Simple signal processing - extract the decision from the signal
        if not full_signal:
            return "No decision available"
        
        # Look for common decision patterns
        signal_lower = full_signal.lower()
        if "buy" in signal_lower:
            return "BUY"
        elif "sell" in signal_lower:
            return "SELL"
        elif "hold" in signal_lower:
            return "HOLD"
        else:
            return full_signal.strip()

    def update_analysts(self, selected_analysts: List[str]) -> None:
        """Update which analysts are included (backward compatibility)."""
        self.selected_analysts = selected_analysts
        # Recompile the graph with new analysts
        self.compiled_graph = self.graph_setup.setup_graph(self.selected_analysts)

    def update_debate_rounds(self, max_debate_rounds: int = None, max_risk_discuss_rounds: int = None) -> None:
        """Update debate and risk discussion limits (backward compatibility)."""
        if max_debate_rounds is not None:
            self.config["max_debate_rounds"] = max_debate_rounds
            self.conditional_logic.max_debate_rounds = max_debate_rounds
        
        if max_risk_discuss_rounds is not None:
            self.config["max_risk_discuss_rounds"] = max_risk_discuss_rounds
            self.conditional_logic.max_risk_discuss_rounds = max_risk_discuss_rounds

    def reflect_and_remember(self, position_returns: float) -> None:
        """Reflect on decisions and update memory (backward compatibility)."""
        # Update memories with reflection using the correct method
        reflection_message = f"Position returns: {position_returns}"
        reflection_tuple = (reflection_message, f"Learn from returns: {position_returns}")
        
        self.bull_memory.add_situations([reflection_tuple])
        self.bear_memory.add_situations([reflection_tuple])
        self.trader_memory.add_situations([reflection_tuple])
        self.invest_judge_memory.add_situations([reflection_tuple])
        self.risk_manager_memory.add_situations([reflection_tuple])


# Optional factory function for backward compatibility
def create_trading_agents_graph(config: Optional[Dict[str, Any]] = None) -> TradingAgentsGraph:
    return TradingAgentsGraph(config)
