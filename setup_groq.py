#!/usr/bin/env python3
"""
Groq API Setup Script for SafeSpace.AI
=====================================

This script helps you set up Groq API access for fast LLM-based toxicity detection
and empathetic message rewriting.

Groq offers:
- FREE API access with generous limits
- Ultra-fast inference (up to 750 tokens/second)
- Multiple models: Llama 3.1, Mixtral, Gemma
- 30,000 free tokens per day for developers

Steps:
1. Get your free Groq API key from https://console.groq.com/
2. Run this script to configure the API
3. Test the integration
"""

import os
import requests
import json
from datetime import datetime

def get_groq_api_key():
    """Get Groq API key from user input or environment"""
    
    # Check if already set in environment
    existing_key = os.environ.get('GROQ_API_KEY')
    if existing_key:
        print(f"✅ Found existing Groq API key: {existing_key[:8]}...")
        use_existing = input("Use existing key? (y/n): ").lower().strip()
        if use_existing in ['y', 'yes', '']:
            return existing_key
    
    print("\n🚀 Groq API Setup")
    print("=" * 50)
    print("1. Go to: https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Navigate to 'API Keys' section")
    print("4. Create a new API key")
    print("5. Copy the key and paste it below")
    print("\nNote: Groq offers 30,000 free tokens per day!")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided!")
        return None
    
    if not api_key.startswith('gsk_'):
        print("⚠️  Warning: Groq API keys typically start with 'gsk_'")
        confirm = input("Continue anyway? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes']:
            return None
    
    return api_key

def test_groq_api(api_key):
    """Test the Groq API connection"""
    
    print("\n🧪 Testing Groq API connection...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple toxicity detection prompt
    data = {
        "model": "llama-3.1-8b-instant",  # Fast, free model
        "messages": [
            {
                "role": "system",
                "content": "You are a content moderator. Analyze if the message contains harassment, toxicity, or harmful content. Respond with just 'TOXIC' or 'SAFE' followed by a brief reason."
            },
            {
                "role": "user", 
                "content": "Analyze this message: 'Hello, how are you today?'"
            }
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            print(f"✅ API Test Successful!")
            print(f"   Response: {answer}")
            print(f"   Model: {result.get('model', 'Unknown')}")
            
            # Test usage info
            usage = result.get('usage', {})
            if usage:
                print(f"   Tokens used: {usage.get('total_tokens', 'Unknown')}")
            
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed! Check your API key.")
            return False
            
        elif response.status_code == 429:
            print("❌ Rate limit exceeded! Try again later.")
            return False
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout! Check your internet connection.")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def save_api_config(api_key):
    """Save API configuration to environment file"""
    
    env_file = ".env"
    env_content = ""
    
    # Read existing .env file if it exists
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add Groq API key
    lines = env_content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith('GROQ_API_KEY='):
            lines[i] = f'GROQ_API_KEY={api_key}'
            updated = True
            break
    
    if not updated:
        lines.append(f'GROQ_API_KEY={api_key}')
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write('\n'.join(line for line in lines if line.strip()))
        f.write('\n')
    
    print(f"✅ API key saved to {env_file}")

def update_app_config():
    """Update app.py to use Groq API"""
    
    print("\n🔧 Updating app.py configuration...")
    
    app_file = "app.py"
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found!")
        return False
    
    try:
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Check if Groq is already configured
        if 'GROQ_API_KEY' in content:
            print("✅ Groq API already configured in app.py")
            return True
        
        # Add Groq configuration comment
        config_comment = """
# Groq API Configuration
# Set GROQ_API_KEY environment variable or in .env file
# Free tier: 30,000 tokens/day, ultra-fast inference
"""
        
        if config_comment not in content:
            # Add near the top after imports
            import_end = content.find('\napp = Flask')
            if import_end != -1:
                content = content[:import_end] + config_comment + content[import_end:]
        
        with open(app_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated app.py with Groq configuration")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

def show_usage_guide():
    """Show how to use Groq API in the application"""
    
    print("\n📖 Groq API Usage Guide")
    print("=" * 50)
    print("✅ Setup complete! Here's how to use Groq in your app:")
    print()
    print("1. ENVIRONMENT SETUP:")
    print("   - API key saved to .env file")
    print("   - Load with: load_dotenv() in app.py")
    print()
    print("2. AVAILABLE MODELS:")
    print("   - llama-3.1-8b-instant (Recommended - fastest)")
    print("   - llama-3.1-70b-versatile (More capable)")
    print("   - mixtral-8x7b-32768 (Good balance)")
    print("   - gemma2-9b-it (Lightweight)")
    print()
    print("3. API LIMITS (FREE TIER):")
    print("   - 30,000 tokens per day")
    print("   - Up to 750 tokens/second")
    print("   - Multiple concurrent requests")
    print()
    print("4. SAMPLE API CALL:")
    print("""
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Your prompt"}],
        "max_tokens": 100,
        "temperature": 0.1
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                           headers=headers, json=data)
    """)
    print()
    print("5. RESTART YOUR APP:")
    print("   python app.py")
    print()

def main():
    """Main setup function"""
    
    print("🚀 SafeSpace.AI - Groq API Setup")
    print("=" * 50)
    print("Setting up ultra-fast, free LLM API for toxicity detection...")
    print()
    
    # Step 1: Get API key
    api_key = get_groq_api_key()
    if not api_key:
        print("❌ Setup cancelled - no API key provided")
        return
    
    # Step 2: Test the API
    if not test_groq_api(api_key):
        print("❌ Setup failed - API test unsuccessful")
        return
    
    # Step 3: Save configuration
    save_api_config(api_key)
    
    # Step 4: Update app configuration
    update_app_config()
    
    # Step 5: Show usage guide
    show_usage_guide()
    
    print("🎉 Groq API setup complete!")
    print("💡 Tip: Groq is extremely fast - perfect for real-time detection!")

if __name__ == "__main__":
    main()