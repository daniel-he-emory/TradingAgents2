#!/usr/bin/env python3
"""
Simple test script to verify the new TradingAgentsGraph implementation.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_trading_graph():
    """Test the simplified TradingAgentsGraph class."""
    print("Testing simplified TradingAgentsGraph...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph, create_trading_agents_graph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Test 1: Direct instantiation with default config
        print("✓ Testing direct instantiation...")
        graph1 = TradingAgentsGraph()
        print("  - Default config instantiation works")
        
        # Test 2: Direct instantiation with custom config
        print("✓ Testing custom config instantiation...")
        config = DEFAULT_CONFIG.copy()
        config["max_debate_rounds"] = 2
        graph2 = TradingAgentsGraph(config=config)
        print("  - Custom config instantiation works")
        
        # Test 3: Factory function
        print("✓ Testing factory function...")
        graph3 = create_trading_agents_graph()
        print("  - Factory function works")
        
        # Test 4: Factory function with custom config
        print("✓ Testing factory function with custom config...")
        graph4 = create_trading_agents_graph(config=config)
        print("  - Factory function with custom config works")
        
        # Test 5: Check that propagate method exists
        print("✓ Testing propagate method...")
        if hasattr(graph1, 'propagate') and callable(getattr(graph1, 'propagate')):
            print("  - Propagate method exists and is callable")
        else:
            print("  ✗ Propagate method missing or not callable")
            return False
        
        # Test 6: Check that components are initialized
        print("✓ Testing component initialization...")
        if hasattr(graph1, 'graph_setup') and hasattr(graph1, 'conditional_logic') and hasattr(graph1, 'propagator'):
            print("  - All components initialized")
        else:
            print("  ✗ Components not properly initialized")
            return False
        
        print("\n🎉 All tests passed! Simplified TradingAgentsGraph is working correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_trading_graph()
    sys.exit(0 if success else 1) 