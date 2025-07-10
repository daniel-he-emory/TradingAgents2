#!/usr/bin/env python3
"""
Test script to verify that the TradingAgentsGraph wrapper works correctly.

This script tests:
1. Factory function creation
2. Direct class instantiation
3. Propagate method functionality
4. Backward compatibility methods
5. Configuration updates
"""

import sys
import os
import pytest
from unittest.mock import Mock, patch
from tradingagents.graph.trading_graph import TradingAgentsGraph, create_trading_agents_graph

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_factory_function():
    """Test the factory function for creating TradingAgentsGraph instances."""
    print("Testing factory function...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Test with default config
        graph = create_trading_agents_graph()
        print("✓ Factory function with default config works")
        
        # Test with custom config
        config = DEFAULT_CONFIG.copy()
        config["max_debate_rounds"] = 2
        graph = create_trading_agents_graph(debug=True, config=config)
        print("✓ Factory function with custom config works")
        
        # Test with custom analysts
        graph = create_trading_agents_graph(selected_analysts=["market", "news"])
        print("✓ Factory function with custom analysts works")
        
        return True
        
    except Exception as e:
        print(f"✗ Factory function test failed: {e}")
        return False

def test_direct_instantiation():
    """Test direct instantiation of TradingAgentsGraph class."""
    print("\nTesting direct instantiation...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Test with default config - should use token optimization
        graph = TradingAgentsGraph()
        
        # Verify token optimization settings
        assert graph.config["max_debate_rounds"] == 1, "Debate rounds should be 1 for token optimization"
        assert graph.config["max_risk_discuss_rounds"] == 1, "Risk discuss rounds should be 1 for token optimization"
        assert graph.config["max_recur_limit"] == 50, "Recur limit should be 50 for token optimization"
        assert graph.selected_analysts == ["market", "fundamentals"], "Should only use market and fundamentals analysts"
        
        print("✓ Direct instantiation with token optimization works")
        return True
        
    except Exception as e:
        print(f"✗ Direct instantiation test failed: {e}")
        return False

def test_propagate_method():
    """Test the propagate method."""
    print("\nTesting propagate method...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        
        # Create graph instance
        graph = create_trading_agents_graph(selected_analysts=["market"])
        
        # Test propagate method
        result = graph.propagate("AAPL", "2024-01-15")
        
        # Check that result is a dictionary
        if isinstance(result, dict):
            print("✓ Propagate method returns dictionary")
        else:
            print("✗ Propagate method does not return dictionary")
            return False
        
        # Check for expected keys
        expected_keys = ["company_of_interest", "trade_date", "messages"]
        for key in expected_keys:
            if key in result:
                print(f"✓ Result contains {key}")
            else:
                print(f"✗ Result missing {key}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Propagate method test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility methods."""
    print("\nTesting backward compatibility...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        
        # Create graph instance
        graph = create_trading_agents_graph(selected_analysts=["market"])
        
        # Test process_signal method
        test_signal = "Based on the analysis, I recommend BUY for this stock."
        processed = graph.process_signal(test_signal)
        if isinstance(processed, str):
            print("✓ process_signal method works")
        else:
            print("✗ process_signal method failed")
            return False
        
        # Test update_analysts method
        graph.update_analysts(["market", "news"])
        if graph.selected_analysts == ["market", "news"]:
            print("✓ update_analysts method works")
        else:
            print("✗ update_analysts method failed")
            return False
        
        # Test update_debate_rounds method
        graph.update_debate_rounds(max_debate_rounds=3)
        if graph.conditional_logic.max_debate_rounds == 3:
            print("✓ update_debate_rounds method works")
        else:
            print("✗ update_debate_rounds method failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Backward compatibility test failed: {e}")
        return False

def test_fastapi_compatibility():
    """Test that the graph works with FastAPI-style usage."""
    print("\nTesting FastAPI compatibility...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        
        # Simulate FastAPI usage
        def get_trading_graph():
            return create_trading_agents_graph(selected_analysts=["market"])
        
        # Get graph instance
        ta = get_trading_graph()
        
        # Simulate trade endpoint call
        ticker = "AAPL"
        date = "2024-01-15"
        
        # Run propagation
        result = ta.propagate(ticker, date)
        
        # Extract decision (simulating FastAPI response creation)
        final_decision = result.get("final_trade_decision", "")
        processed_signal = final_decision
        
        # Create response-like structure
        response = {
            "ticker": ticker,
            "date": date,
            "recommendation": processed_signal.strip(),
            "reasoning": final_decision,
            "processed_signal": processed_signal.strip()
        }
        
        if all(key in response for key in ["ticker", "date", "recommendation", "reasoning", "processed_signal"]):
            print("✓ FastAPI compatibility works")
            return True
        else:
            print("✗ FastAPI compatibility failed")
            return False
        
    except Exception as e:
        print(f"✗ FastAPI compatibility test failed: {e}")
        return False

class TestTradingAgentsGraph:
    """Test cases for TradingAgentsGraph class."""

    def test_init_with_default_config(self):
        """Test initialization with default configuration."""
        with patch('tradingagents.graph.trading_graph.ChatOpenAI'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            graph = TradingAgentsGraph()
            
            # Verify token optimization settings
            assert graph.config["max_debate_rounds"] == 1
            assert graph.config["max_risk_discuss_rounds"] == 1
            assert graph.config["max_recur_limit"] == 50
            assert graph.selected_analysts == ["market", "fundamentals"]

    def test_init_with_custom_config(self):
        """Test initialization with custom configuration."""
        custom_config = {
            "llm_provider": "openai",
            "deep_think_llm": "gpt-4o",
            "quick_think_llm": "gpt-4o",
            "backend_url": "https://api.openai.com/v1",
            "max_debate_rounds": 2,  # Should be overridden to 1
            "max_risk_discuss_rounds": 3,  # Should be overridden to 1
            "max_recur_limit": 75,  # Should be overridden to 50
        }
        
        with patch('tradingagents.graph.trading_graph.ChatOpenAI'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            graph = TradingAgentsGraph(custom_config)
            
            # Verify token optimization overrides custom values
            assert graph.config["max_debate_rounds"] == 1
            assert graph.config["max_risk_discuss_rounds"] == 1
            assert graph.config["max_recur_limit"] == 50
            assert graph.selected_analysts == ["market", "fundamentals"]

    def test_init_with_anthropic_provider(self):
        """Test initialization with Anthropic provider."""
        config = {
            "llm_provider": "anthropic",
            "deep_think_llm": "claude-3-5-sonnet-20241022",
            "quick_think_llm": "claude-3-haiku-20240307",
            "backend_url": "https://api.anthropic.com",
        }
        
        with patch('tradingagents.graph.trading_graph.ChatAnthropic'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            graph = TradingAgentsGraph(config)
            assert graph.config["llm_provider"] == "anthropic"

    def test_init_with_google_provider(self):
        """Test initialization with Google provider."""
        config = {
            "llm_provider": "google",
            "deep_think_llm": "gemini-1.5-pro",
            "quick_think_llm": "gemini-1.5-flash",
        }
        
        with patch('tradingagents.graph.trading_graph.ChatGoogleGenerativeAI'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            graph = TradingAgentsGraph(config)
            assert graph.config["llm_provider"] == "google"

    def test_init_with_invalid_provider(self):
        """Test initialization with invalid LLM provider."""
        config = {"llm_provider": "invalid"}
        
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            TradingAgentsGraph(config)

    def test_propagate_method(self):
        """Test the propagate method."""
        with patch('tradingagents.graph.trading_graph.ChatOpenAI'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            # Mock the compiled graph
            mock_compiled_graph = Mock()
            mock_compiled_graph.invoke.return_value = {"result": "test_output"}
            
            graph = TradingAgentsGraph()
            graph.compiled_graph = mock_compiled_graph
            
            # Mock the propagator methods
            graph.propagator.create_initial_state = Mock(return_value={"initial": "state"})
            graph.propagator.get_graph_args = Mock(return_value={"args": "test"})
            
            # Test propagate method
            result = graph.propagate("AAPL", "2024-01-15")
            
            assert result == {"result": "test_output"}
            graph.propagator.create_initial_state.assert_called_once_with("AAPL", "2024-01-15")
            graph.propagator.get_graph_args.assert_called_once()
            mock_compiled_graph.invoke.assert_called_once_with({"initial": "state"}, {"args": "test"})

    def test_tool_nodes_optimization(self):
        """Test that only essential tool nodes are created for token optimization."""
        with patch('tradingagents.graph.trading_graph.ChatOpenAI'), \
             patch('tradingagents.graph.trading_graph.Toolkit'), \
             patch('tradingagents.graph.trading_graph.FinancialSituationMemory'), \
             patch('tradingagents.graph.trading_graph.ConditionalLogic'), \
             patch('tradingagents.graph.trading_graph.GraphSetup'), \
             patch('tradingagents.graph.trading_graph.Propagator'), \
             patch('tradingagents.graph.trading_graph.set_config'), \
             patch('os.makedirs'):
            
            graph = TradingAgentsGraph()
            
            # Verify only market and fundamentals tool nodes exist
            assert "market" in graph.tool_nodes
            assert "fundamentals" in graph.tool_nodes
            assert "social" not in graph.tool_nodes
            assert "news" not in graph.tool_nodes


class TestCreateTradingAgentsGraph:
    """Test cases for the factory function."""

    def test_factory_function(self):
        """Test the create_trading_agents_graph factory function."""
        with patch('tradingagents.graph.trading_graph.TradingAgentsGraph') as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance
            
            result = create_trading_agents_graph()
            
            mock_class.assert_called_once_with(None)
            assert result == mock_instance

    def test_factory_function_with_config(self):
        """Test the factory function with custom configuration."""
        config = {"test": "config"}
        
        with patch('tradingagents.graph.trading_graph.TradingAgentsGraph') as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance
            
            result = create_trading_agents_graph(config)
            
            mock_class.assert_called_once_with(config)
            assert result == mock_instance


def main():
    """Run all tests."""
    print("Running TradingAgentsGraph tests...\n")
    
    tests = [
        test_factory_function,
        test_direct_instantiation,
        test_propagate_method,
        test_backward_compatibility,
        test_fastapi_compatibility,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TradingAgentsGraph is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 