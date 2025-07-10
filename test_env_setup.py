#!/usr/bin/env python3
"""
Test script to verify environment variable setup.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_env_loading():
    """Test that environment variables are loaded correctly."""
    print("Testing environment variable loading...")
    
    try:
        # Test 1: Check if dotenv is available
        from dotenv import load_dotenv
        print("✓ python-dotenv is available")
        
        # Test 2: Load environment variables
        load_dotenv()
        print("✓ Environment variables loaded from .env file")
        
        # Test 3: Check if OpenAI API key is set
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            print("✓ OpenAI API key is set")
        else:
            print("⚠️  OpenAI API key not set or is placeholder")
            print("   Run 'python setup_env.py' to set it up")
        
        # Test 4: Check other environment variables
        env_vars = [
            'LLM_PROVIDER',
            'DEEP_THINK_LLM', 
            'QUICK_THINK_LLM',
            'BACKEND_URL',
            'MAX_DEBATE_ROUNDS',
            'MAX_RISK_DISCUSS_ROUNDS',
            'MAX_RECUR_LIMIT',
            'ONLINE_TOOLS'
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                print(f"✓ {var} = {value}")
            else:
                print(f"⚠️  {var} not set")
        
        # Test 5: Test default config loading
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✓ Default config loaded successfully")
        
        # Test 6: Check if config uses environment variables
        config_llm_provider = DEFAULT_CONFIG.get('llm_provider')
        env_llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        
        if config_llm_provider == env_llm_provider:
            print("✓ Config correctly uses environment variables")
        else:
            print(f"⚠️  Config mismatch: config={config_llm_provider}, env={env_llm_provider}")
        
        print("\n🎉 Environment setup test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed the requirements: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_fastapi_env_loading():
    """Test that FastAPI app loads environment variables correctly."""
    print("\nTesting FastAPI environment loading...")
    
    try:
        # Import the app module to trigger environment loading
        import app
        print("✓ FastAPI app loads environment variables correctly")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI environment loading failed: {e}")
        return False

def main():
    """Run all environment tests."""
    print("Environment Variable Setup Test")
    print("=" * 40)
    
    test1_passed = test_env_loading()
    test2_passed = test_fastapi_env_loading()
    
    if test1_passed and test2_passed:
        print("\n✅ All environment tests passed!")
        print("Your environment is configured correctly.")
        return True
    else:
        print("\n❌ Some environment tests failed.")
        print("Please check your .env file and configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 