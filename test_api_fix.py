#!/usr/bin/env python3
"""
Test script to verify the API key fix and basic trading functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test if environment variables are loaded correctly"""
    print("=== Environment Variables Test ===")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    llm_provider = os.getenv('LLM_PROVIDER')
    backend_url = os.getenv('BACKEND_URL')
    
    print(f"LLM_PROVIDER: {llm_provider}")
    print(f"BACKEND_URL: {backend_url}")
    print(f"OpenAI API Key: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"OpenAI API Key (first 10 chars): {openai_key[:10] if openai_key else 'None'}")
    
    return bool(openai_key and llm_provider and backend_url)

def test_trading_graph_init():
    """Test if TradingAgentsGraph can be initialized"""
    print("\n=== Trading Graph Initialization Test ===")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        
        # Create trading graph instance
        graph = TradingAgentsGraph()
        print("✅ TradingAgentsGraph initialized successfully")
        
        # Check if LLMs are created
        print(f"Deep thinking LLM: {type(graph.deep_thinking_llm).__name__}")
        print(f"Quick thinking LLM: {type(graph.quick_thinking_llm).__name__}")
        
        return True, graph
        
    except Exception as e:
        print(f"❌ Failed to initialize TradingAgentsGraph: {e}")
        return False, None

def test_basic_functionality(graph):
    """Test basic trading functionality with a simple request"""
    print("\n=== Basic Functionality Test ===")
    
    try:
        # Test with AAPL for today's date
        result = graph.propagate(
            company_name="AAPL",
            trade_date="2025-07-01",
            deep_think_model="gpt-4o-mini",  # Use a cheaper model for testing
            debate_rounds=1
        )
        
        print("✅ Trading analysis completed successfully")
        print(f"Final decision: {result.get('final_trade_decision', 'No decision')[:100]}...")
        print(f"Recommendation: {result.get('recommendation', 'No recommendation')}")
        print(f"Confidence: {result.get('confidence', 'No confidence')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Trading analysis failed: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Trading Agents API Key Fix")
    print("=" * 50)
    
    # Test 1: Environment variables
    env_ok = test_env_variables()
    if not env_ok:
        print("❌ Environment variables test failed")
        return False
    
    # Test 2: Graph initialization
    init_ok, graph = test_trading_graph_init()
    if not init_ok:
        print("❌ Graph initialization test failed")
        return False
    
    # Test 3: Basic functionality
    func_ok = test_basic_functionality(graph)
    if not func_ok:
        print("❌ Basic functionality test failed")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Your app should work now.")
    print("You can refresh your localhost application.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)