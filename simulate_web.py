#!/usr/bin/env python3
"""
Simulate the exact bulk analysis process as done in the web interface
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_web_bulk_analysis():
    """Simulate the exact bulk analysis as done in the web route"""
    
    # Your exact input text
    text_input = """Hello team, hope everyone is doing well today!
Great job on the presentation yesterday.
You're an idiot and I hate working with you.
Thanks for helping with the project.
This is stupid and a waste of time.
I appreciate everyone's collaboration."""
    
    # Split into messages (same as web interface)
    messages = [line.strip() for line in text_input.split('\n') if line.strip()]
    
    print("🌐 SIMULATING WEB INTERFACE BULK ANALYSIS")
    print("="*70)
    print("📋 INPUT MESSAGES:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg}")
    
    # Import the exact functions used in the web interface
    from app import (
        classify_message_toxicity_with_explanation,
        generate_contextual_empathy_rewrite,
        log_analysis
    )
    
    print("\n🔄 PROCESSING (same as web interface):")
    print("-" * 70)
    
    results = []
    
    for i, message in enumerate(messages, 1):
        print(f"\nAnalyzing message {i}/{len(messages)}: {message[:50]}...")
        classification = classify_message_toxicity_with_explanation(message)
        
        # For toxic messages, use contextual intelligence (same as web code)
        if classification["label"] == "toxic":
            print(f"🧠 Applying contextual analysis for toxic message...")
            contextual_result = generate_contextual_empathy_rewrite(message, messages, i-1)
            
            result = {
                "message_id": i,
                "message": message,
                "label": classification["label"],
                "score": classification["score"],
                "confidence": classification.get("confidence", classification["score"]),
                "method": classification.get("method", "unknown"),
                "explanation": classification.get("explanation"),
                "rewrite": contextual_result.get('rewrite'),
                "rewrite_type": contextual_result.get('type'),
                "rewrite_reason": contextual_result.get('reason'),
                "recommended_action": "Remove Message" if contextual_result.get('type') == 'remove' else "Rewrite Message"
            }
        else:
            result = {
                "message_id": i,
                "message": message,
                "label": classification["label"],
                "score": classification["score"],
                "confidence": classification.get("confidence", classification["score"]),
                "method": classification.get("method", "unknown"),
                "explanation": classification.get("explanation"),
                "rewrite": None,
                "rewrite_type": None,
                "rewrite_reason": None,
                "recommended_action": "Safe"
            }
        
        results.append(result)
        
        # Print detailed results
        status_emoji = "🚨" if classification["label"] == "toxic" else "✅"
        print(f"  {status_emoji} {classification['label'].upper()} (score: {classification['score']:.3f})")
        
        if classification.get("explanation"):
            print(f"  💡 Explanation: {classification['explanation'][:80]}...")
            
        if classification["label"] == "toxic":
            if result.get("rewrite_type") == "remove":
                print(f"  🗑️ Contextual decision: REMOVE ({result.get('rewrite_reason')})")
            elif result.get("rewrite"):
                print(f"  ✏️ Contextual rewrite: {result['rewrite']}")
                print(f"  📝 Reason: {result.get('rewrite_reason')}")
    
    # Generate cleaned text (same as web interface)
    print(f"\n📝 GENERATING CLEANED TEXT:")
    print("-" * 70)
    
    cleaned_messages = []
    removed_count = 0
    rewritten_count = 0
    
    for result in results:
        if result["label"] == "toxic":
            if result.get("rewrite_type") == "remove":
                print(f"Removing message {result['message_id']}: '{result['message'][:50]}...'")
                removed_count += 1
                continue
            elif result.get("rewrite"):
                print(f"Rewriting message {result['message_id']}: '{result['rewrite']}'")
                cleaned_messages.append(result["rewrite"])
                rewritten_count += 1
            else:
                cleaned_messages.append(result["message"])
        else:
            print(f"Keeping message {result['message_id']}: '{result['message'][:50]}...'")
            cleaned_messages.append(result["message"])
    
    cleaned_text = "\n".join(cleaned_messages)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Removed: {removed_count}, Rewritten: {rewritten_count}")
    print(f"\n🎯 CLEANED TEXT OUTPUT:")
    print("="*70)
    print(cleaned_text)
    print("="*70)

if __name__ == "__main__":
    simulate_web_bulk_analysis()