#!/usr/bin/env python3
"""
Quick API Test to Debug the Failure Issue
"""

import os
import requests
import time

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not available - using system environment variables")

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

def test_groq_single_call():
    """Test a single Groq API call to debug issues"""
    
    if not GROQ_API_KEY:
        print("❌ No Groq API key found!")
        return False
    
    print(f"🔑 Using Groq API key: {GROQ_API_KEY[:8]}...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    test_message = "You're like a bug in every piece of code — persistent and extremely annoying."
    
    system_prompt = """You are an expert content moderator. Analyze the message for harassment, toxicity, hate speech, or harmful content.

Consider context and intent carefully. Be precise and avoid false positives.

Respond with EXACTLY this format:
TOXIC: [brief reason] OR SAFE: [brief reason]

Be especially careful with:
- Casual language that might seem rude but isn't harmful
- Context-dependent statements
- Sarcasm or humor
- Animal comparisons used as insults"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this message: '{test_message}'"}
        ],
        "max_tokens": 100,
        "temperature": 0.1
    }
    
    print("📡 Testing API call...")
    start_time = time.time()
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        elapsed_time = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed_time:.2f}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            tokens = result.get('usage', {}).get('total_tokens', 0)
            
            print(f"✅ Success!")
            print(f"   Response: {answer}")
            print(f"   Tokens used: {tokens}")
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed! Check your API key.")
            print(f"   Response: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("❌ Rate limit exceeded!")
            print(f"   Response: {response.text}")
            return False
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout! (>15 seconds)")
        return False
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_multiple_rapid_calls():
    """Test multiple rapid calls to check rate limiting"""
    
    print("\n🚀 Testing rapid API calls...")
    
    for i in range(5):
        print(f"\n📞 Call {i+1}/5:")
        success = test_groq_single_call()
        if not success:
            print(f"❌ Failed on call {i+1}")
            break
        
        # Small delay between calls
        time.sleep(0.5)

if __name__ == "__main__":
    print("🔧 Groq API Debugging Test")
    print("=" * 50)
    
    # Test single call
    test_groq_single_call()
    
    # Test multiple calls
    test_multiple_rapid_calls()