#!/usr/bin/env python3
"""
SafeSpace.AI - Comprehensive Toxicity Testing Script
===================================================

This script tests 100 toxic samples from test_messages_new.txt using the current
Groq-powered detection system and generates a detailed CSV report.

Features:
- Tests each message with the hybrid detection system (rules + Groq API)
- Provides toxicity scores, confidence levels, and explanations
- Generates empathetic rewrites for toxic messages
- Exports results to CSV for analysis
- Tracks API usage and performance metrics
"""

import os
import csv
import json
import time
import re
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not available - using system environment variables")

# Import the detection functions from app_groq
import sys
sys.path.append('.')

# Import required libraries
import requests

# Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
TEST_FILE = 'test_messages_new.txt'
OUTPUT_CSV = f'toxicity_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def call_groq_api(text, task="toxicity"):
    """Call Groq API for ultra-fast toxicity detection or rewriting"""
    
    if not GROQ_API_KEY:
        return None
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        if task == "toxicity":
            # Toxicity detection prompt
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
                "model": "llama-3.1-8b-instant",  # Fastest free model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this message: '{text}'"}
                ],
                "max_tokens": 100,
                "temperature": 0.1
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content'].strip()
                
                # Parse the response
                if answer.startswith('TOXIC:'):
                    reason = answer[6:].strip()
                    return {
                        'is_toxic': True,
                        'confidence': 0.95,
                        'reason': reason,
                        'source': 'groq',
                        'tokens_used': result.get('usage', {}).get('total_tokens', 0)
                    }
                elif answer.startswith('SAFE:'):
                    reason = answer[5:].strip()
                    return {
                        'is_toxic': False,
                        'confidence': 0.95,
                        'reason': reason,
                        'source': 'groq',
                        'tokens_used': result.get('usage', {}).get('total_tokens', 0)
                    }
                
        elif task == "rewrite":
            # Empathetic rewriting prompt
            system_prompt = """You are an empathetic communication coach. Transform the given message into a kind, respectful, and constructive version while preserving the core intent.

Guidelines:
- Keep the same general meaning
- Use positive, respectful language
- Remove any harsh, offensive, or toxic elements
- Make it sound natural and human
- Be concise and clear

Respond with ONLY the rewritten message, nothing else."""

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Rewrite this message to be more empathetic and respectful: '{text}'"}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                rewritten = result['choices'][0]['message']['content'].strip()
                rewritten = rewritten.strip('"').strip()
                
                if len(rewritten) > 5 and rewritten.lower() != text.lower():
                    return {
                        'rewrite': rewritten,
                        'tokens_used': result.get('usage', {}).get('total_tokens', 0)
                    }
                    
    except Exception as e:
        print(f"🔴 Groq API error: {e}")
        return None
    
    return None

# Rule-based toxicity patterns for comparison
TOXICITY_PATTERNS = [
    # Direct insults
    (r'\b(idiot|stupid|dumb|moron|retard|fool|loser)\b', 0.9, "Contains direct insults"),
    
    # Animal comparisons as insults
    (r'\b(donkey|pig|dog|rat|snake)\s+you\b', 0.95, "Uses animal comparison as insult"),
    (r'\byou.*\b(donkey|pig|dog|rat|snake)\b', 0.95, "Uses animal comparison as insult"),
    
    # Profanity and harsh language
    (r'\b(damn|hell|crap|shit|fuck)\b', 0.7, "Contains profanity"),
    
    # Threats or aggressive language
    (r'\b(shut up|go away|get lost|kill yourself)\b', 0.8, "Dismissive/aggressive language"),
    
    # Personal attacks
    (r'\b(ugly|fat|worthless|pathetic|disgusting)\b', 0.85, "Personal attack language"),
    
    # Intelligence/capability attacks
    (r'\b(intelligence|IQ|brain|smart|clever).*\b(lacking|missing|absent|zero|none)\b', 0.8, "Intelligence attack"),
    (r'\b(fastest sperm|mess.*up|messed up)\b', 0.85, "Personal/biological insult"),
    
    # System/tech metaphor insults
    (r'\b(install.*intelligence|firmware|database|storage|corruption)\b', 0.75, "Tech metaphor insult"),
]

def classify_with_rules(text):
    """Fast rule-based classification for comparison"""
    text_lower = text.lower().strip()
    
    max_confidence = 0
    best_reason = ""
    
    # Check for toxicity patterns
    for pattern, confidence, reason in TOXICITY_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            if confidence > max_confidence:
                max_confidence = confidence
                best_reason = reason
    
    if max_confidence > 0:
        return {
            'is_toxic': True,
            'confidence': max_confidence,
            'reason': best_reason,
            'source': 'rules'
        }
    
    # Default to uncertain
    return {
        'is_toxic': False,
        'confidence': 0.3,
        'reason': "No toxic patterns detected by rules",
        'source': 'rules'
    }

def test_single_message(message, message_id):
    """Test a single message with both rule-based and API detection"""
    
    print(f"\n🧪 Testing Message {message_id}")
    print(f"📝 Text: '{message[:60]}...' " if len(message) > 60 else f"📝 Text: '{message}'")
    
    results = {
        'message_id': message_id,
        'message': message,
        'message_length': len(message)
    }
    
    start_time = time.time()
    
    # Test with rule-based detection
    rule_result = classify_with_rules(message)
    results.update({
        'rule_is_toxic': rule_result['is_toxic'],
        'rule_confidence': rule_result['confidence'],
        'rule_reason': rule_result['reason']
    })
    
    # Test with Groq API
    if GROQ_API_KEY:
        api_result = call_groq_api(message, "toxicity")
        if api_result:
            results.update({
                'groq_is_toxic': api_result['is_toxic'],
                'groq_confidence': api_result['confidence'],
                'groq_reason': api_result['reason'],
                'groq_tokens': api_result.get('tokens_used', 0)
            })
            
            # Generate rewrite if toxic
            if api_result['is_toxic']:
                rewrite_result = call_groq_api(message, "rewrite")
                if rewrite_result:
                    results.update({
                        'empathy_rewrite': rewrite_result['rewrite'],
                        'rewrite_tokens': rewrite_result.get('tokens_used', 0)
                    })
        else:
            results.update({
                'groq_is_toxic': None,
                'groq_confidence': None,
                'groq_reason': "API call failed",
                'groq_tokens': 0
            })
    else:
        results.update({
            'groq_is_toxic': None,
            'groq_confidence': None,
            'groq_reason': "No API key",
            'groq_tokens': 0
        })
    
    # Calculate processing time
    results['processing_time_seconds'] = round(time.time() - start_time, 2)
    
    # Determine final classification (prefer API if available)
    if results.get('groq_is_toxic') is not None:
        results['final_is_toxic'] = results['groq_is_toxic']
        results['final_confidence'] = results['groq_confidence']
        results['final_source'] = 'groq'
    else:
        results['final_is_toxic'] = results['rule_is_toxic']
        results['final_confidence'] = results['rule_confidence']
        results['final_source'] = 'rules'
    
    # Print summary
    final_label = "🔴 TOXIC" if results['final_is_toxic'] else "✅ SAFE"
    confidence = results['final_confidence']
    print(f"   Result: {final_label} ({confidence:.1%} confidence)")
    print(f"   Time: {results['processing_time_seconds']}s")
    
    return results

def load_test_messages():
    """Load test messages from file"""
    messages = []
    
    try:
        with open(TEST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    # Remove quotes if present
                    message = line.strip('"').strip("'").strip()
                    if message:
                        messages.append(message)
        
        print(f"📁 Loaded {len(messages)} test messages from {TEST_FILE}")
        return messages
        
    except FileNotFoundError:
        print(f"❌ File {TEST_FILE} not found!")
        return []
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return []

def save_results_to_csv(results):
    """Save test results to CSV file"""
    
    if not results:
        print("❌ No results to save")
        return
    
    # Define CSV columns
    fieldnames = [
        'message_id', 'message', 'message_length',
        'final_is_toxic', 'final_confidence', 'final_source',
        'rule_is_toxic', 'rule_confidence', 'rule_reason',
        'groq_is_toxic', 'groq_confidence', 'groq_reason', 'groq_tokens',
        'empathy_rewrite', 'rewrite_tokens',
        'processing_time_seconds'
    ]
    
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                # Ensure all fields exist
                row = {}
                for field in fieldnames:
                    row[field] = result.get(field, '')
                writer.writerow(row)
        
        print(f"✅ Results saved to {OUTPUT_CSV}")
        return OUTPUT_CSV
        
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return None

def generate_summary_report(results):
    """Generate summary statistics"""
    
    if not results:
        return
    
    total_messages = len(results)
    
    # Count toxic vs safe
    toxic_count = sum(1 for r in results if r.get('final_is_toxic'))
    safe_count = total_messages - toxic_count
    
    # Calculate accuracy metrics
    rule_toxic = sum(1 for r in results if r.get('rule_is_toxic'))
    groq_toxic = sum(1 for r in results if r.get('groq_is_toxic'))
    
    # Performance metrics
    total_time = sum(r.get('processing_time_seconds', 0) for r in results)
    avg_time = total_time / total_messages if total_messages > 0 else 0
    
    total_tokens = sum(r.get('groq_tokens', 0) + r.get('rewrite_tokens', 0) for r in results)
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY REPORT")
    print("="*60)
    print(f"📝 Total Messages Tested: {total_messages}")
    print(f"🔴 Classified as TOXIC: {toxic_count} ({toxic_count/total_messages*100:.1f}%)")
    print(f"✅ Classified as SAFE: {safe_count} ({safe_count/total_messages*100:.1f}%)")
    print()
    print("🔍 Detection Method Comparison:")
    print(f"   Rules detected toxic: {rule_toxic} ({rule_toxic/total_messages*100:.1f}%)")
    print(f"   Groq detected toxic: {groq_toxic} ({groq_toxic/total_messages*100:.1f}%)")
    print()
    print("⚡ Performance Metrics:")
    print(f"   Total processing time: {total_time:.1f} seconds")
    print(f"   Average time per message: {avg_time:.2f} seconds")
    print(f"   Total API tokens used: {total_tokens}")
    print(f"   Average tokens per message: {total_tokens/total_messages:.1f}")
    print()
    print(f"💾 Detailed results saved to: {OUTPUT_CSV}")
    print("="*60)

def main():
    """Main testing function"""
    
    print("🚀 SafeSpace.AI - Comprehensive Toxicity Testing")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Groq API: {'✅ Available' if GROQ_API_KEY else '❌ Not configured'}")
    print(f"📁 Test File: {TEST_FILE}")
    print(f"📊 Output File: {OUTPUT_CSV}")
    print()
    
    # Load test messages
    messages = load_test_messages()
    if not messages:
        print("❌ No messages to test!")
        return
    
    print(f"🧪 Starting test of {len(messages)} messages...")
    print("⏱️  This may take several minutes with API calls...")
    
    # Test each message
    results = []
    
    for i, message in enumerate(messages, 1):
        try:
            result = test_single_message(message, i)
            results.append(result)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n⚠️ Testing interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error testing message {i}: {e}")
            continue
    
    print(f"\n✅ Testing completed! Processed {len(results)} messages")
    
    # Save results
    if results:
        save_results_to_csv(results)
        generate_summary_report(results)
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    main()