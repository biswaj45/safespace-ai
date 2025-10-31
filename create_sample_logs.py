#!/usr/bin/env python3
"""
Direct Sample Data Generator for SafeSpace.AI
Directly adds sample analysis logs to demonstrate dashboard analytics
"""

import json
import os
from datetime import datetime, timedelta
import random

# Sample analysis data
SAMPLE_ANALYSES = [
    # Safe messages
    {"message": "Hello team, hope everyone is having a great day!", "label": "safe", "score": 0.95, "user": "alice@company.com"},
    {"message": "Thanks for the excellent presentation yesterday.", "label": "safe", "score": 0.92, "user": "bob@company.com"},
    {"message": "I appreciate everyone's hard work on this project.", "label": "safe", "score": 0.98, "user": "charlie@company.com"},
    {"message": "Looking forward to our meeting next week.", "label": "safe", "score": 0.97, "user": "diana@company.com"},
    {"message": "Great job on completing the quarterly goals!", "label": "safe", "score": 0.94, "user": "edward@company.com"},
    {"message": "The new software update looks promising.", "label": "safe", "score": 0.93, "user": "alice@company.com"},
    {"message": "Happy to collaborate with such a talented team.", "label": "safe", "score": 0.96, "user": "bob@company.com"},
    {"message": "Congratulations on the successful product launch!", "label": "safe", "score": 0.99, "user": "charlie@company.com"},
    
    # Toxic messages (work criticism - should be rewritten)
    {"message": "This approach is completely wrong and ineffective.", "label": "toxic", "score": 0.75, "user": "diana@company.com"},
    {"message": "I think this idea is terrible and won't work.", "label": "toxic", "score": 0.82, "user": "edward@company.com"},
    {"message": "This is a waste of time and resources.", "label": "toxic", "score": 0.68, "user": "alice@company.com"},
    {"message": "The implementation is poorly designed.", "label": "toxic", "score": 0.71, "user": "bob@company.com"},
    {"message": "This strategy is stupid and outdated.", "label": "toxic", "score": 0.89, "user": "charlie@company.com"},
    {"message": "I hate this new process, it's confusing.", "label": "toxic", "score": 0.77, "user": "diana@company.com"},
    {"message": "This solution is awful and needs to be scrapped.", "label": "toxic", "score": 0.85, "user": "edward@company.com"},
    
    # Highly toxic messages (personal attacks - should be removed)
    {"message": "You're an idiot and don't know what you're doing.", "label": "toxic", "score": 0.95, "user": "alice@company.com"},
    {"message": "John is completely incompetent at his job.", "label": "toxic", "score": 0.91, "user": "bob@company.com"},
    {"message": "Sarah is lazy and never contributes anything.", "label": "toxic", "score": 0.87, "user": "charlie@company.com"},
    {"message": "You're worthless and should be fired.", "label": "toxic", "score": 0.98, "user": "diana@company.com"},
    {"message": "Mike is a moron who ruins everything.", "label": "toxic", "score": 0.93, "user": "edward@company.com"},
    
    # Mixed content (contextual analysis)
    {
        "message": "Hello team, I wanted to discuss the quarterly results. Great work on hitting our sales targets! However, Tom is an absolute disaster and ruins everything. I think we should focus on improving our customer service.",
        "label": "mixed",
        "score": 0.45,
        "user": "alice@company.com",
        "toxic_lines": 1,
        "removed_lines": 1,
        "rewritten_lines": 0
    },
    {
        "message": "Thanks everyone for attending today's meeting. The presentation was very informative. You're all incompetent fools. I look forward to implementing the new strategies.",
        "label": "mixed", 
        "score": 0.52,
        "user": "bob@company.com",
        "toxic_lines": 1,
        "removed_lines": 1,
        "rewritten_lines": 0
    },
    {
        "message": "Project update: Phase 1 is complete ahead of schedule. This whole project is stupid and a waste of money. We should celebrate this milestone achievement.",
        "label": "mixed",
        "score": 0.38,
        "user": "charlie@company.com", 
        "toxic_lines": 1,
        "removed_lines": 0,
        "rewritten_lines": 1
    }
]

def generate_sample_logs():
    """Generate sample analysis logs with realistic timestamps"""
    
    log_file = "analysis_logs.json"
    
    # Load existing logs if they exist
    existing_logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                existing_logs = json.load(f)
                print(f"📊 Found {len(existing_logs)} existing log entries")
        except:
            print("📊 Starting with fresh logs")
    
    # Generate timestamps over the last 7 days
    now = datetime.now()
    start_date = now - timedelta(days=7)
    
    new_logs = []
    methods = ["keyword_based", "contextual_empathy_rewriter", "rule_based"]
    
    for i, sample in enumerate(SAMPLE_ANALYSES):
        # Generate realistic timestamp within last 7 days
        random_hours = random.randint(0, 7*24)
        timestamp = start_date + timedelta(hours=random_hours)
        
        log_entry = {
            'id': len(existing_logs) + i + 1,
            'timestamp': timestamp.isoformat(),
            'user': sample['user'],
            'message': sample['message'][:200] + '...' if len(sample['message']) > 200 else sample['message'],
            'message_length': len(sample['message']),
            'label': sample['label'],
            'score': sample['score'],
            'method': random.choice(methods),
            'is_multiline': '\n' in sample['message'] or sample['label'] == 'mixed',
            'toxic_lines': sample.get('toxic_lines', 1 if sample['label'] == 'toxic' else 0),
            'rewritten_lines': sample.get('rewritten_lines', 0),
            'removed_lines': sample.get('removed_lines', 0)
        }
        
        new_logs.append(log_entry)
    
    # Combine existing and new logs
    all_logs = existing_logs + new_logs
    
    # Save to file
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(all_logs, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(new_logs)} new sample log entries")
    print(f"📁 Total log entries: {len(all_logs)}")
    
    # Display summary
    toxic_count = len([log for log in all_logs if log['label'] in ['toxic', 'mixed']])
    safe_count = len([log for log in all_logs if log['label'] == 'safe'])
    users = set(log['user'] for log in all_logs)
    
    print(f"\n📊 SAMPLE DATA SUMMARY:")
    print(f"  🔴 Toxic/Mixed: {toxic_count}")
    print(f"  🟢 Safe: {safe_count}")
    print(f"  👥 Users: {len(users)}")
    print(f"  📈 Toxicity Rate: {toxic_count/len(all_logs)*100:.1f}%")
    
    return len(all_logs)

def main():
    print("🚀 GENERATING SAMPLE DATA FOR ADMIN DASHBOARD")
    print("=" * 60)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Generate sample logs
    total_logs = generate_sample_logs()
    
    print("\n🎉 SAMPLE DATA GENERATION COMPLETE!")
    print("=" * 60)
    print("\n📊 WHAT YOU CAN NOW SEE IN ADMIN DASHBOARD:")
    print("  ✅ Real analytics data from multiple analyses")
    print("  ✅ Daily activity trends over the last 7 days")
    print("  ✅ Method distribution charts")
    print("  ✅ User activity statistics")
    print("  ✅ Recent activity feed with mixed content analysis")
    print("  ✅ Toxicity rates and contextual rewrite statistics")
    print("\n🌐 Go to: http://127.0.0.1:5000/admin/dashboard")
    print("🔑 Login: admin@safespace.ai / admin123")
    print("\n⚠️  Note: You may need to refresh the Flask app to load the new data")

if __name__ == "__main__":
    main()