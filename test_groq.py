#!/usr/bin/env python3
"""
Test Groq API integration without PyTorch dependencies
"""

import os
import requests
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not available - using system environment variables")

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

def test_groq_toxicity_detection():
    """Test Groq API for toxicity detection"""
    
    if not GROQ_API_KEY:
        print("❌ No Groq API key found!")
        return False
    
    print(f"🔑 Using Groq API key: {GROQ_API_KEY[:8]}...")
    
    test_messages = [
        "Hello, how are you today?",  # Should be SAFE
        "You're such an idiot!",      # Should be TOXIC
        "if there is a donkey you are that",  # Should be TOXIC (animal comparison)
        "i wish you all the best"     # Should be SAFE
    ]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an expert content moderator. Analyze the message for harassment, toxicity, hate speech, or harmful content.

Consider context and intent carefully. Be precise and avoid false positives.

Respond with EXACTLY this format:
TOXIC: [brief reason] OR SAFE: [brief reason]

Be especially careful with:
- Casual language that might seem rude but isn't harmful
- Context-dependent statements
- Sarcasm or humor
- Animal comparisons used as insults"""

    print("\n🧪 Testing Groq API Toxicity Detection:")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this message: '{message}'"}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content'].strip()
                
                # Parse the response
                if answer.startswith('TOXIC:'):
                    status = "🔴 TOXIC"
                    reason = answer[6:].strip()
                elif answer.startswith('SAFE:'):
                    status = "✅ SAFE"
                    reason = answer[5:].strip()
                else:
                    status = "❓ UNCLEAR"
                    reason = answer
                
                print(f"   Result: {status}")
                print(f"   Reason: {reason}")
                
                # Show usage
                usage = result.get('usage', {})
                if usage:
                    print(f"   Tokens: {usage.get('total_tokens', 'Unknown')}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return True

def test_groq_empathy_rewriter():
    """Test Groq API for empathetic rewriting"""
    
    if not GROQ_API_KEY:
        print("❌ No Groq API key found!")
        return False
    
    test_messages = [
        "You're such an idiot!",
        "This is stupid and pointless",
        "if there is a donkey you are that"
    ]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an empathetic communication coach. Transform the given message into a kind, respectful, and constructive version while preserving the core intent.

Guidelines:
- Keep the same general meaning
- Use positive, respectful language
- Remove any harsh, offensive, or toxic elements
- Make it sound natural and human
- Be concise and clear

Respond with ONLY the rewritten message, nothing else."""

    print("\n✏️ Testing Groq API Empathy Rewriter:")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Original: '{message}'")
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Rewrite this message to be more empathetic and respectful: '{message}'"}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                rewritten = result['choices'][0]['message']['content'].strip()
                rewritten = rewritten.strip('"').strip()
                
                print(f"   Rewritten: '{rewritten}'")
                
                # Show usage
                usage = result.get('usage', {})
                if usage:
                    print(f"   Tokens: {usage.get('total_tokens', 'Unknown')}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return True

if __name__ == "__main__":
    print("🚀 SafeSpace.AI - Groq API Testing")
    print("=" * 50)
    
    # Test toxicity detection
    test_groq_toxicity_detection()
    
    # Test empathy rewriter
    test_groq_empathy_rewriter()
    
    print("\n🎉 Groq API testing complete!")
    print("💡 Groq is extremely fast - perfect for real-time detection!")