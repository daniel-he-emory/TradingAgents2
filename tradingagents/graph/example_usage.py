# TradingAgents/graph/example_usage.py

"""
Example usage of the TradingAgentsGraph wrapper class.

This example shows how to use the simplified interface that wraps
GraphSetup, Propagator, and ConditionalLogic into a single .propagate() method.
"""

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph


def create_trading_agents_graph():
    """Create and configure a TradingAgentsGraph instance."""
    
    # Create the TradingAgentsGraph wrapper with default config
    # The new interface automatically handles all initialization
    graph = TradingAgentsGraph(config=DEFAULT_CONFIG)
    
    return graph


def run_analysis(company_name: str, trade_date: str):
    """Run a complete trading analysis using the wrapper."""
    
    # Create the graph
    graph = create_trading_agents_graph()
    
    # Execute the analysis with a single method call
    result = graph.propagate(company_name, trade_date)
    
    print(f"Analysis completed for {company_name} on {trade_date}")
    print(f"Final decision: {result.get('final_trade_decision', 'No decision made')}")
    
    return result


def example_with_updates():
    """Example showing how to update configuration and re-run."""
    
    # Create initial graph
    graph = create_trading_agents_graph()
    
    # Run initial analysis
    result1 = graph.propagate("AAPL", "2024-01-15")
    
    # Update to include social media analysis
    graph.update_analysts(["market", "social", "news", "fundamentals"])
    
    # Run updated analysis
    result2 = graph.propagate("AAPL", "2024-01-15")
    
    # Update debate rounds
    graph.update_debate_rounds(max_debate_rounds=3, max_risk_discuss_rounds=3)
    
    # Run with more debate rounds
    result3 = graph.propagate("AAPL", "2024-01-15")
    
    return result1, result2, result3


if __name__ == "__main__":
    # Example usage
    result = run_analysis("AAPL", "2024-01-15")
    print("Analysis result:", result) 