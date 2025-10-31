#!/usr/bin/env python3
"""
SafeSpace.AI - CSV Analysis Script
=================================

Analyzes the test results CSV to identify API failures and patterns.
"""

import pandas as pd
import os
from datetime import datetime

def analyze_csv_results():
    """Analyze the CSV file to identify API failures and patterns"""
    
    csv_file = "toxicity_test_results_20251031_133524.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file {csv_file} not found!")
        return
    
    print("🔍 Analyzing Test Results CSV")
    print("=" * 50)
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        total_messages = len(df)
        print(f"📊 Total Messages: {total_messages}")
        
        # Analyze API failures
        api_failed = df[df['groq_reason'] == 'API call failed']
        api_success = df[df['groq_reason'] != 'API call failed']
        api_success = api_success[df['groq_reason'].notna()]
        
        failed_count = len(api_failed)
        success_count = len(api_success)
        
        print(f"\n🔴 API Failures: {failed_count} ({failed_count/total_messages*100:.1f}%)")
        print(f"✅ API Success: {success_count} ({success_count/total_messages*100:.1f}%)")
        
        # Analyze failure patterns by message number
        print(f"\n📈 Failure Pattern Analysis:")
        failure_ranges = []
        
        failed_ids = api_failed['message_id'].tolist()
        if failed_ids:
            print(f"   Failed message IDs: {failed_ids[:10]}..." if len(failed_ids) > 10 else f"   Failed message IDs: {failed_ids}")
            
            # Find consecutive failure ranges
            consecutive_start = None
            for i, msg_id in enumerate(failed_ids):
                if i == 0:
                    consecutive_start = msg_id
                elif msg_id != failed_ids[i-1] + 1:
                    # End of consecutive range
                    if consecutive_start is not None:
                        if consecutive_start == failed_ids[i-1]:
                            failure_ranges.append(f"{consecutive_start}")
                        else:
                            failure_ranges.append(f"{consecutive_start}-{failed_ids[i-1]}")
                    consecutive_start = msg_id
            
            # Handle last range
            if consecutive_start is not None:
                if consecutive_start == failed_ids[-1]:
                    failure_ranges.append(f"{consecutive_start}")
                else:
                    failure_ranges.append(f"{consecutive_start}-{failed_ids[-1]}")
        
        print(f"   Failure ranges: {', '.join(failure_ranges)}")
        
        # Analyze final classification sources
        print(f"\n🔍 Final Classification Sources:")
        source_counts = df['final_source'].value_counts()
        for source, count in source_counts.items():
            print(f"   {source}: {count} ({count/total_messages*100:.1f}%)")
        
        # Analyze processing times
        print(f"\n⏱️  Processing Time Analysis:")
        successful_times = api_success['processing_time_seconds'].tolist()
        failed_times = api_failed['processing_time_seconds'].tolist()
        
        if successful_times:
            avg_success_time = sum(successful_times) / len(successful_times)
            print(f"   Avg time (API success): {avg_success_time:.2f}s")
        
        if failed_times:
            avg_failed_time = sum(failed_times) / len(failed_times)
            print(f"   Avg time (API failed): {avg_failed_time:.2f}s")
        
        # Analyze token usage
        print(f"\n🪙 Token Usage Analysis:")
        total_tokens = df['groq_tokens'].fillna(0).sum()
        successful_tokens = api_success['groq_tokens'].fillna(0).sum()
        
        print(f"   Total tokens used: {total_tokens}")
        print(f"   Successful API tokens: {successful_tokens}")
        
        if success_count > 0:
            avg_tokens = successful_tokens / success_count
            print(f"   Avg tokens per successful call: {avg_tokens:.1f}")
        
        # Analyze toxicity detection differences
        print(f"\n🎯 Toxicity Detection Analysis:")
        
        # Count toxic detections by source
        groq_toxic = len(df[(df['groq_is_toxic'] == True)])
        rule_toxic = len(df[(df['rule_is_toxic'] == True)])
        final_toxic = len(df[(df['final_is_toxic'] == True)])
        
        print(f"   Groq detected toxic: {groq_toxic}")
        print(f"   Rules detected toxic: {rule_toxic}")
        print(f"   Final toxic count: {final_toxic}")
        
        # Analyze discrepancies
        print(f"\n🔄 Detection Discrepancies:")
        
        # Cases where rules detected toxic but API failed
        rule_toxic_api_failed = df[(df['rule_is_toxic'] == True) & (df['groq_reason'] == 'API call failed')]
        print(f"   Rules toxic + API failed: {len(rule_toxic_api_failed)}")
        
        if len(rule_toxic_api_failed) > 0:
            print("   Examples:")
            for idx, row in rule_toxic_api_failed.head(3).iterrows():
                print(f"     - MSG {row['message_id']}: \"{row['message'][:50]}...\"")
                print(f"       Rule reason: {row['rule_reason']}")
        
        # Cases where API and rules disagreed (when API worked)
        disagreements = api_success[api_success['groq_is_toxic'] != api_success['rule_is_toxic']]
        print(f"\n   API vs Rules disagreements: {len(disagreements)}")
        
        if len(disagreements) > 0:
            print("   Examples:")
            for idx, row in disagreements.head(3).iterrows():
                groq_result = "TOXIC" if row['groq_is_toxic'] else "SAFE"
                rule_result = "TOXIC" if row['rule_is_toxic'] else "SAFE"
                print(f"     - MSG {row['message_id']}: Groq={groq_result}, Rules={rule_result}")
                print(f"       \"{row['message'][:50]}...\"")
        
        # Identify potential issues
        print(f"\n⚠️  Potential Issues Identified:")
        
        issues = []
        
        if failed_count > total_messages * 0.5:
            issues.append(f"High API failure rate ({failed_count/total_messages*100:.1f}%)")
        
        if failed_times and avg_failed_time < 0.2:
            issues.append("API failures are happening too quickly (likely network/auth issues)")
        
        if successful_times and any(t > 1.0 for t in successful_times):
            slow_calls = sum(1 for t in successful_times if t > 1.0)
            issues.append(f"{slow_calls} API calls took >1 second (potential timeout issues)")
        
        if len(issues) == 0:
            issues.append("No major issues detected")
        
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        recommendations = []
        
        if failed_count > 10:
            recommendations.append("Add retry logic with exponential backoff for failed API calls")
            recommendations.append("Implement better error handling and logging for API failures")
        
        if failed_times and avg_failed_time < 0.2:
            recommendations.append("Check API key validity and network connectivity")
            recommendations.append("Add API key validation before batch processing")
        
        recommendations.append("Consider implementing a hybrid fallback to rules when API fails consistently")
        recommendations.append("Add API rate limiting and request queuing")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
    except Exception as e:
        print(f"❌ Error analyzing CSV: {e}")

if __name__ == "__main__":
    analyze_csv_results()