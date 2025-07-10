#!/usr/bin/env python3
"""
Setup script to help users create their .env file with the OpenAI API key.
"""

import os
import sys

def create_env_file():
    """Create a .env file with the user's OpenAI API key."""
    
    print("Setting up environment variables for Trading Agents...")
    print("=" * 50)
    
    # Check if .env file already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Get OpenAI API key from user
    print("\nPlease enter your OpenAI API key:")
    print("You can find it at: https://platform.openai.com/api-keys")
    api_key = input("OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ OpenAI API key is required!")
        return
    
    # Create .env file content
    env_content = f"""# Trading Agents Environment Variables

# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# LLM Provider Settings
LLM_PROVIDER=openai
DEEP_THINK_LLM=gpt-4o
QUICK_THINK_LLM=gpt-4o
BACKEND_URL=https://api.openai.com/v1

# Debate and Discussion Settings
MAX_DEBATE_ROUNDS=1
MAX_RISK_DISCUSS_ROUNDS=1
MAX_RECUR_LIMIT=100

# Tool Settings
ONLINE_TOOLS=true

# Data Settings
DATA_DIR=/Users/yluo/Documents/Code/ScAI/FR1-data
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
        print("📁 Location: .env")
        print("\n🔒 Security Note: Make sure .env is in your .gitignore file to keep your API key secure.")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return
    
    # Verify the file was created
    if os.path.exists('.env'):
        print("\n✅ Environment setup complete!")
        print("You can now run the Trading Agents application.")
    else:
        print("❌ Failed to create .env file.")

def check_env_file():
    """Check if .env file exists and has required variables."""
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Run 'python setup_env.py' to create it.")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not set or is placeholder!")
        print("Please update your .env file with your actual API key.")
        return False
    
    print("✅ .env file found and configured correctly!")
    return True

def main():
    """Main function."""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_env_file()
    else:
        create_env_file()

if __name__ == "__main__":
    main() 