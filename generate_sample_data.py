#!/usr/bin/env python3
"""
Sample Data Generator for SafeSpace.AI Admin Dashboard
Creates realistic user inputs to demonstrate analytics features
"""

import requests
import json
import time
import random

# API endpoint
BASE_URL = "http://127.0.0.1:5000"

# Sample messages with different toxicity levels
SAMPLE_MESSAGES = [
    # Safe messages
    "Hello team, hope everyone is having a great day!",
    "Thanks for the excellent presentation yesterday.",
    "I appreciate everyone's hard work on this project.",
    "Looking forward to our meeting next week.",
    "Great job on completing the quarterly goals!",
    "The new software update looks promising.",
    "Happy to collaborate with such a talented team.",
    "Congratulations on the successful product launch!",
    
    # Work criticism (should be rewritten)
    "This approach is completely wrong and ineffective.",
    "I think this idea is terrible and won't work.",
    "This is a waste of time and resources.",
    "The implementation is poorly designed.",
    "This strategy is stupid and outdated.",
    "I hate this new process, it's confusing.",
    "This solution is awful and needs to be scrapped.",
    
    # Personal attacks (should be removed)
    "You're an idiot and don't know what you're doing.",
    "John is completely incompetent at his job.",
    "Sarah is lazy and never contributes anything.",
    "You're worthless and should be fired.",
    "Mike is a moron who ruins everything.",
    "You people are all stupid and useless.",
    
    # Mixed content (contextual analysis)
    """Hello team, I wanted to discuss the quarterly results.
    Great work on hitting our sales targets!
    However, Tom is an absolute disaster and ruins everything.
    I think we should focus on improving our customer service.
    The new marketing campaign looks really promising.
    But this budget proposal is completely idiotic.""",
    
    """Thanks everyone for attending today's meeting.
    The presentation was very informative and well-structured.
    You're all incompetent fools who can't do anything right.
    I look forward to implementing the new strategies.
    Let's schedule a follow-up meeting next week.""",
    
    """Project update: Phase 1 is complete ahead of schedule.
    The development team has done excellent work.
    This whole project is stupid and a waste of money.
    We should celebrate this milestone achievement.
    Looking forward to Phase 2 implementation."""
]

# Sample users
USERS = [
    "alice@company.com",
    "bob@company.com", 
    "charlie@company.com",
    "diana@company.com",
    "edward@company.com"
]

def simulate_real_time_analysis(message, user_email="demo@safespace.ai"):
    """Simulate real-time analysis"""
    try:
        # First login (if needed) or use demo mode
        response = requests.post(f"{BASE_URL}/api/analyze-realtime", 
                               json={"text": message},
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Real-time analysis: {result.get('label', 'unknown')} (score: {result.get('score', 0):.3f})")
            return result
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception during analysis: {e}")
        return None

def simulate_bulk_analysis(messages, filename="sample_data.txt"):
    """Simulate bulk file analysis"""
    try:
        # Create a temporary file content
        content = "\n".join(messages)
        
        # Simulate file upload
        files = {'file_upload': (filename, content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/analyze", files=files, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Bulk analysis completed for {len(messages)} messages")
            return True
        else:
            print(f"❌ Bulk analysis error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during bulk analysis: {e}")
        return False

def main():
    print("🚀 GENERATING SAMPLE DATA FOR ADMIN DASHBOARD")
    print("=" * 60)
    
    # Wait for Flask app to be ready
    print("⏳ Waiting for Flask app to be ready...")
    time.sleep(2)
    
    # Test connection
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Flask app not accessible. Make sure it's running at http://127.0.0.1:5000")
            return
    except:
        print("❌ Cannot connect to Flask app. Make sure it's running at http://127.0.0.1:5000")
        return
    
    print("✅ Flask app is accessible!")
    print()
    
    # Generate real-time analyses
    print("📝 GENERATING REAL-TIME ANALYSES")
    print("-" * 40)
    
    for i, message in enumerate(SAMPLE_MESSAGES[:15], 1):
        user = random.choice(USERS)
        print(f"{i:2d}. Analyzing: {message[:60]}...")
        
        result = simulate_real_time_analysis(message, user)
        if result:
            time.sleep(0.5)  # Realistic delay between analyses
        
        if i % 5 == 0:
            print(f"    📊 Completed {i} analyses")
    
    print()
    
    # Generate bulk analyses
    print("📁 GENERATING BULK ANALYSES")
    print("-" * 40)
    
    # Create different bulk sets
    bulk_sets = [
        ("team_chat_1.txt", SAMPLE_MESSAGES[8:13]),
        ("feedback_session.txt", SAMPLE_MESSAGES[13:18]),
        ("project_meeting.txt", SAMPLE_MESSAGES[18:22]),
        ("mixed_conversation.txt", [SAMPLE_MESSAGES[-3], SAMPLE_MESSAGES[-2], SAMPLE_MESSAGES[-1]])
    ]
    
    for filename, messages in bulk_sets:
        print(f"📄 Processing {filename} ({len(messages)} messages)")
        simulate_bulk_analysis(messages, filename)
        time.sleep(1)
    
    print()
    print("🎉 SAMPLE DATA GENERATION COMPLETE!")
    print("=" * 60)
    print()
    print("📊 WHAT YOU CAN NOW SEE IN ADMIN DASHBOARD:")
    print("  ✅ Real analytics data from multiple analyses")
    print("  ✅ Daily activity trends")
    print("  ✅ Method distribution charts") 
    print("  ✅ User activity statistics")
    print("  ✅ Recent activity feed")
    print("  ✅ Toxicity rates and scores")
    print()
    print("🌐 Go to: http://127.0.0.1:5000/admin/dashboard")
    print("🔑 Login: admin@safespace.ai / admin123")

if __name__ == "__main__":
    main()