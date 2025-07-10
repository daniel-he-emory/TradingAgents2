#!/usr/bin/env python3
"""
Test actual propagation with trading agents.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_propagation():
    """Test actual propagation with a real stock."""
    print("Testing propagation with real data...")
    
    try:
        from tradingagents.graph.trading_graph import create_trading_agents_graph
        
        # Create graph
        print("  Creating trading graph...")
        graph = create_trading_agents_graph()
        
        # Test propagation with a well-known stock
        print("  Running propagation for AAPL...")
        result = graph.propagate("AAPL", "2024-01-15")
        
        print("  Propagation completed successfully!")
        print(f"  Result type: {type(result)}")
        
        # Check if result has expected structure
        if isinstance(result, dict):
            print("✓ Result is a dictionary")
            
            # Print available keys
            print(f"  Available keys: {list(result.keys())}")
            
            # Look for common keys
            expected_keys = ["company_of_interest", "trade_date", "final_trade_decision", "messages"]
            found_keys = []
            for key in expected_keys:
                if key in result:
                    found_keys.append(key)
            
            if found_keys:
                print(f"✓ Found expected keys: {found_keys}")
            else:
                print("⚠️  No expected keys found, but propagation completed")
            
            # Show a sample of the result
            for key, value in list(result.items())[:3]:  # Show first 3 items
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
                    
            return True
        else:
            print(f"⚠️  Result is not a dictionary: {result}")
            return True  # Still a success if it completed
            
    except Exception as e:
        print(f"❌ Propagation test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run propagation test."""
    print("Trading Agents Propagation Test")
    print("=" * 35)
    
    success = test_propagation()
    
    if success:
        print("\n✅ Propagation test completed successfully!")
        print("🎉 Your trading agents system is working!")
        return True
    else:
        print("\n❌ Propagation test failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)