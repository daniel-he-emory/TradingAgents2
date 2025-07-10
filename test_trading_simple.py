#!/usr/bin/env python3
"""
Simple test script to verify trading agents work without external dependencies.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_trading_graph_import():
    """Test that we can import the trading graph components."""
    print("Testing trading graph imports...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph, create_trading_agents_graph
        print("✓ TradingAgentsGraph imported successfully")
        
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✓ Default config imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config_loading():
    """Test that configuration loads correctly with Anthropic."""
    print("\nTesting configuration loading...")
    
    try:
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Check LLM provider
        llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        if llm_provider == 'anthropic':
            print("✓ LLM provider set to anthropic")
        else:
            print(f"⚠️  LLM provider is {llm_provider}, expected anthropic")
        
        # Check API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and not api_key.startswith('your_anthropic'):
            print("✓ Anthropic API key is set")
        else:
            print("❌ Anthropic API key not properly configured")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_simple_graph_creation():
    """Test basic graph creation."""
    print("\nTesting graph creation...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        
        # Try to create a graph with minimal configuration
        print("  Creating trading graph...")
        graph = create_trading_agents_graph()
        
        if graph is not None:
            print("✓ Trading graph created successfully")
            
            # Check if it has the expected attributes
            if hasattr(graph, 'propagate'):
                print("✓ Graph has propagate method")
            else:
                print("❌ Graph missing propagate method")
                return False
                
            return True
        else:
            print("❌ Graph creation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Graph creation failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all simple tests."""
    print("Simple Trading Agents Test")
    print("=" * 30)
    
    tests = [
        test_trading_graph_import,
        test_config_loading,
        test_simple_graph_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All simple tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)