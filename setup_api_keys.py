#!/usr/bin/env python3
"""
Setup script for configuring free LLM API keys
Run this to configure your API keys for better detection and rewriting
"""

import os

def setup_huggingface_api():
    """Setup Hugging Face API key (Free tier: 1000 requests/month)"""
    print("\n🤗 HUGGING FACE SETUP")
    print("=" * 50)
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Create a free account if needed")
    print("3. Generate a new token (Read access is sufficient)")
    print("4. Copy the token")
    
    api_key = input("\nEnter your Hugging Face API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Set environment variable for current session
        os.environ['HUGGINGFACE_API_KEY'] = api_key
        
        # Also write to .env file for persistence
        with open('.env', 'a') as f:
            f.write(f"\nHUGGINGFACE_API_KEY={api_key}")
        
        print("✅ Hugging Face API key configured!")
        return True
    else:
        print("⏭️ Skipping Hugging Face setup")
        return False

def setup_groq_api():
    """Setup Groq API key (Fast inference, free tier available)"""
    print("\n⚡ GROQ SETUP")
    print("=" * 50)
    print("1. Go to: https://console.groq.com/keys")
    print("2. Create a free account if needed")
    print("3. Generate a new API key")
    print("4. Copy the key")
    
    api_key = input("\nEnter your Groq API key (or press Enter to skip): ").strip()
    
    if api_key:
        os.environ['GROQ_API_KEY'] = api_key
        
        with open('.env', 'a') as f:
            f.write(f"\nGROQ_API_KEY={api_key}")
        
        print("✅ Groq API key configured!")
        return True
    else:
        print("⏭️ Skipping Groq setup")
        return False

def test_api_setup():
    """Test the configured APIs"""
    print("\n🧪 TESTING API SETUP")
    print("=" * 50)
    
    # Import the API functions from app.py
    try:
        from app import call_huggingface_api
        
        test_message = "This is a test message"
        
        if os.environ.get('HUGGINGFACE_API_KEY'):
            print("Testing Hugging Face API...")
            result = call_huggingface_api(test_message, "toxicity")
            if result:
                print("✅ Hugging Face API working!")
            else:
                print("❌ Hugging Face API failed")
        
        print("\n🎉 Setup complete! You can now use API-based detection.")
        
    except Exception as e:
        print(f"❌ Error testing APIs: {e}")
        print("You may need to restart the Flask app to use the new API keys.")

def main():
    """Main setup function"""
    print("🌐 FREE LLM API SETUP")
    print("=" * 60)
    print("This script helps you configure free API keys for better")
    print("toxicity detection and empathetic rewriting.")
    print("\nChoose your preferred APIs (you can set up multiple):")
    
    apis_configured = 0
    
    # Setup options
    if input("\n1. Setup Hugging Face API? (y/n): ").lower().startswith('y'):
        if setup_huggingface_api():
            apis_configured += 1
    
    if input("\n2. Setup Groq API? (y/n): ").lower().startswith('y'):
        if setup_groq_api():
            apis_configured += 1
    
    if apis_configured > 0:
        print(f"\n✅ {apis_configured} API(s) configured successfully!")
        
        if input("\n3. Test API setup now? (y/n): ").lower().startswith('y'):
            test_api_setup()
    else:
        print("\n⚠️ No APIs configured. The system will use rule-based detection only.")
        print("You can run this script again anytime to add API keys.")
    
    print("\n🚀 You can now start the Flask app with API-based detection!")
    print("Run: python app.py")

if __name__ == "__main__":
    main()