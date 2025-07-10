#!/usr/bin/env python3
"""
Test script to verify LLM API connectivity for OpenAI and Anthropic.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_connectivity():
    """Test OpenAI API connectivity."""
    print("Testing OpenAI API connectivity...")
    
    try:
        import openai
        
        # Get API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key.startswith('your_openai_api_key'):
            print("❌ OpenAI API key not properly configured")
            return False
            
        # Initialize client
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        if response.choices and response.choices[0].message.content:
            print("✓ OpenAI API connection successful")
            print(f"  Response: {response.choices[0].message.content.strip()}")
            return True
        else:
            print("❌ OpenAI API returned empty response")
            return False
            
    except ImportError:
        print("❌ OpenAI library not installed")
        return False
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def test_anthropic_connectivity():
    """Test Anthropic API connectivity."""
    print("\nTesting Anthropic API connectivity...")
    
    try:
        import anthropic
        
        # Get API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key.startswith('your_anthropic_api_key'):
            print("❌ Anthropic API key not properly configured")
            return False
            
        # Initialize client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test with a simple request
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say 'API test successful'"}]
        )
        
        if response.content and response.content[0].text:
            print("✓ Anthropic API connection successful")
            print(f"  Response: {response.content[0].text.strip()}")
            return True
        else:
            print("❌ Anthropic API returned empty response")
            return False
            
    except ImportError:
        print("❌ Anthropic library not installed")
        return False
    except Exception as e:
        print(f"❌ Anthropic API test failed: {e}")
        return False

def main():
    """Run all LLM connectivity tests."""
    print("LLM API Connectivity Test")
    print("=" * 30)
    
    openai_success = test_openai_connectivity()
    anthropic_success = test_anthropic_connectivity()
    
    print(f"\n📊 Test Results:")
    print(f"OpenAI API: {'✅ Working' if openai_success else '❌ Failed'}")
    print(f"Anthropic API: {'✅ Working' if anthropic_success else '❌ Failed'}")
    
    if openai_success or anthropic_success:
        print("\n✅ At least one LLM provider is working!")
        return True
    else:
        print("\n❌ No LLM providers are working. Check your API keys.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)