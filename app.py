from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session
import os
import pandas as pd
import re
import csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'safespace_ai_secret_key_2024')  # For flash messages

# Configure for production
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

# For now, use a simple keyword-based approach as fallback
# We'll replace this with the real model once dependencies are resolved
TOXIC_KEYWORDS = [
    'hate', 'stupid', 'idiot', 'moron', 'dumb', 'kill', 'die', 'shut up',
    'worthless', 'loser', 'pathetic', 'disgusting', 'awful', 'terrible'
]

def classify_message_toxicity_simple(message):
    """Simple keyword-based toxicity detection as fallback"""
    message_lower = message.lower()
    
    # Count toxic keywords
    toxic_count = 0
    for keyword in TOXIC_KEYWORDS:
        if keyword in message_lower:
            toxic_count += 1
    
    # Simple scoring based on keyword presence
    if toxic_count > 0:
        # Higher score for more keywords
        score = min(0.9, 0.5 + (toxic_count * 0.2))
        return {
            "label": "toxic",
            "score": round(score, 3),
            "confidence": round(score, 3),
            "keywords_found": toxic_count
        }
    else:
        return {
            "label": "safe", 
            "score": 0.9,
            "confidence": 0.9,
            "keywords_found": 0
        }

# Try to load the real model, fall back to simple method if it fails
print("🔄 Attempting to load toxicity detection model...")
try:
    from transformers import pipeline
    toxicity_classifier = pipeline(
        "text-classification", 
        model="unitary/toxic-bert",
        return_all_scores=True
    )
    print("✅ Advanced toxicity detection model loaded successfully!")
    USE_ADVANCED_MODEL = True
except Exception as e:
    print(f"⚠️  Could not load advanced model: {str(e)}")
    print("🔄 Using simple keyword-based detection as fallback...")
    toxicity_classifier = None
    USE_ADVANCED_MODEL = False

def classify_message_toxicity(message):
    """Classify a single message for toxicity"""
    if USE_ADVANCED_MODEL and toxicity_classifier:
        try:
            # Get predictions for the message
            results = toxicity_classifier(message)
            
            # The model returns scores for both TOXIC and NON_TOXIC
            # Find the highest scoring prediction
            toxic_score = 0.0
            non_toxic_score = 0.0
            
            for result in results[0]:  # results is a list of lists
                if result['label'] == 'TOXIC':
                    toxic_score = result['score']
                elif result['label'] == 'NON_TOXIC':
                    non_toxic_score = result['score']
            
            # Determine the final classification
            if toxic_score > non_toxic_score:
                return {
                    "label": "toxic",
                    "score": round(toxic_score, 3),
                    "confidence": round(toxic_score, 3),
                    "method": "advanced_model"
                }
            else:
                return {
                    "label": "safe",
                    "score": round(non_toxic_score, 3),
                    "confidence": round(non_toxic_score, 3),
                    "method": "advanced_model"
                }
                
        except Exception as e:
            print(f"❌ Error with advanced model, falling back to simple: {str(e)}")
            return classify_message_toxicity_simple(message)
    
    # Use simple method as fallback
    result = classify_message_toxicity_simple(message)
    result["method"] = "keyword_based"
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    messages = []
    
    # Check if file was uploaded
    if 'file_upload' in request.files:
        file = request.files['file_upload']
        if file and file.filename != '':
            filename = file.filename.lower()
            
            try:
                if filename.endswith('.txt'):
                    # Read text file
                    content = file.read().decode('utf-8')
                    messages = [line.strip() for line in content.split('\n') if line.strip()]
                    print(f"📁 Loaded {len(messages)} messages from TXT file: {file.filename}")
                    
                elif filename.endswith('.csv'):
                    # Read CSV file
                    df = pd.read_csv(file)
                    # Try to find a column with messages (common column names)
                    message_columns = ['message', 'text', 'content', 'chat', 'msg']
                    message_col = None
                    
                    for col in message_columns:
                        if col in df.columns:
                            message_col = col
                            break
                    
                    if message_col:
                        messages = df[message_col].dropna().astype(str).tolist()
                        print(f"📁 Loaded {len(messages)} messages from CSV file: {file.filename} (column: {message_col})")
                    else:
                        # If no common column found, use first column
                        messages = df.iloc[:, 0].dropna().astype(str).tolist()
                        print(f"📁 Loaded {len(messages)} messages from CSV file: {file.filename} (first column)")
                        
                else:
                    flash('Please upload a .txt or .csv file only.')
                    return redirect(url_for('home'))
                    
            except Exception as e:
                print(f"❌ Error reading file: {str(e)}")
                flash(f'Error reading file: {str(e)}')
                return redirect(url_for('home'))
    
    # Check if text was pasted in textarea
    elif request.form.get('text_input'):
        text_input = request.form.get('text_input').strip()
        if text_input:
            messages = [line.strip() for line in text_input.split('\n') if line.strip()]
            print(f"📝 Loaded {len(messages)} messages from textarea input")
    
    # If no input provided
    if not messages:
        flash('Please upload a file or paste some text to analyze.')
        return redirect(url_for('home'))
    
    # Print messages to console for now
    print("\n" + "="*50)
    print("📋 MESSAGES TO ANALYZE:")
    print("="*50)
    for i, message in enumerate(messages, 1):
        print(f"{i:3d}: {message}")
    print("="*50)
    print(f"✅ Total messages loaded: {len(messages)}")
    
    # Classify each message for toxicity
    print("\n🤖 Running toxicity analysis...")
    results = []
    
    for i, message in enumerate(messages, 1):
        print(f"Analyzing message {i}/{len(messages)}: {message[:50]}...")
        classification = classify_message_toxicity(message)
        
        result = {
            "message_id": i,
            "message": message,
            "label": classification["label"],
            "score": classification["score"],
            "confidence": classification.get("confidence", classification["score"]),
            "method": classification.get("method", "unknown"),
            "recommended_action": "Warn User" if classification["label"] == "toxic" else "Safe"
        }
        results.append(result)
        
        # Print result to console
        status_emoji = "🚨" if classification["label"] == "toxic" else "✅"
        print(f"  {status_emoji} {classification['label'].upper()} (score: {classification['score']:.3f})")
    
    print(f"\n📊 Analysis complete! {len(results)} messages processed.")
    
    # Calculate summary statistics
    toxic_count = sum(1 for r in results if r["label"] == "toxic")
    safe_count = len(results) - toxic_count
    toxicity_rate = (toxic_count / len(results)) * 100 if results else 0
    
    print(f"\n📈 Summary: {toxic_count} toxic, {safe_count} safe ({toxicity_rate:.1f}% toxicity rate)")
    
    # Prepare summary data for template
    summary = {
        "total_messages": len(results),
        "toxic_messages": toxic_count,
        "safe_messages": safe_count,
        "toxicity_rate": round(toxicity_rate, 1),
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method_breakdown": {
            "advanced_model": sum(1 for r in results if r.get("method") == "advanced_model"),
            "keyword_based": sum(1 for r in results if r.get("method") == "keyword_based")
        }
    }
    
    # Store results in session for export
    session['last_results'] = results
    session['last_summary'] = summary
    
    # Render results dashboard
    return render_template('results.html', results=results, summary=summary)

@app.route('/export-csv')
def export_csv():
    """Export analysis results as CSV file"""
    # Get results from session
    results = session.get('last_results', [])
    summary = session.get('last_summary', {})
    
    if not results:
        flash('No results to export. Please analyze some messages first.')
        return redirect(url_for('home'))
    
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header with summary information
    writer.writerow(['SafeSpace.AI - Workplace Harassment Detection Results'])
    writer.writerow(['Generated:', summary.get('analysis_timestamp', 'Unknown')])
    writer.writerow(['Total Messages:', summary.get('total_messages', 0)])
    writer.writerow(['Toxic Messages:', summary.get('toxic_messages', 0)])
    writer.writerow(['Safe Messages:', summary.get('safe_messages', 0)])
    writer.writerow(['Toxicity Rate:', f"{summary.get('toxicity_rate', 0)}%"])
    writer.writerow([])  # Empty row
    
    # Write detailed results header
    writer.writerow(['Message ID', 'Message', 'Label', 'Confidence Score', 'Detection Method', 'Recommended Action'])
    
    # Write results data
    for result in results:
        writer.writerow([
            result.get('message_id', ''),
            result.get('message', ''),
            result.get('label', ''),
            result.get('score', ''),
            result.get('method', ''),
            result.get('recommended_action', '')
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=safespace-ai-results-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    
    return response

@app.route('/export-summary')
def export_summary():
    """Export detailed summary report"""
    summary = session.get('last_summary', {})
    results = session.get('last_results', [])
    
    if not results:
        flash('No results to export. Please analyze some messages first.')
        return redirect(url_for('home'))
    
    # Create detailed summary content
    output = StringIO()
    writer = csv.writer(output)
    
    # Summary Report Header
    writer.writerow(['SafeSpace.AI - Detailed Summary Report'])
    writer.writerow(['=' * 50])
    writer.writerow(['Analysis Date:', summary.get('analysis_timestamp', 'Unknown')])
    writer.writerow([])
    
    # Overall Statistics
    writer.writerow(['OVERALL STATISTICS'])
    writer.writerow(['-' * 20])
    writer.writerow(['Total Messages Analyzed:', summary.get('total_messages', 0)])
    writer.writerow(['Toxic Messages Found:', summary.get('toxic_messages', 0)])
    writer.writerow(['Safe Messages:', summary.get('safe_messages', 0)])
    writer.writerow(['Overall Toxicity Rate:', f"{summary.get('toxicity_rate', 0)}%"])
    writer.writerow([])
    
    # Detection Method Breakdown
    method_breakdown = summary.get('method_breakdown', {})
    writer.writerow(['DETECTION METHOD BREAKDOWN'])
    writer.writerow(['-' * 30])
    writer.writerow(['Advanced AI Model:', method_breakdown.get('advanced_model', 0)])
    writer.writerow(['Keyword-Based Detection:', method_breakdown.get('keyword_based', 0)])
    writer.writerow([])
    
    # Toxic Messages Details
    toxic_messages = [r for r in results if r.get('label') == 'toxic']
    writer.writerow(['TOXIC MESSAGES DETECTED'])
    writer.writerow(['-' * 25])
    writer.writerow(['Count:', len(toxic_messages)])
    
    if toxic_messages:
        writer.writerow([])
        writer.writerow(['Message ID', 'Message Preview', 'Confidence Score', 'Detection Method'])
        for msg in toxic_messages:
            preview = msg.get('message', '')[:50] + '...' if len(msg.get('message', '')) > 50 else msg.get('message', '')
            writer.writerow([
                msg.get('message_id', ''),
                preview,
                msg.get('score', ''),
                msg.get('method', '')
            ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=safespace-ai-summary-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    
    return response

@app.route('/test')
def test_results():
    """Test route to show sample results dashboard"""
    # Sample test data to demonstrate the dashboard
    test_results = [
        {
            "message_id": 1,
            "message": "Hello team, hope everyone is doing well today!",
            "label": "safe",
            "score": 0.95,
            "confidence": 0.95,
            "method": "advanced_model",
            "recommended_action": "Safe"
        },
        {
            "message_id": 2,
            "message": "You're an idiot and I hate working with you.",
            "label": "toxic",
            "score": 0.87,
            "confidence": 0.87,
            "method": "advanced_model",
            "recommended_action": "Warn User"
        },
        {
            "message_id": 3,
            "message": "Great job on the presentation yesterday.",
            "label": "safe",
            "score": 0.92,
            "confidence": 0.92,
            "method": "advanced_model",
            "recommended_action": "Safe"
        },
        {
            "message_id": 4,
            "message": "This is stupid and a waste of time.",
            "label": "toxic",
            "score": 0.73,
            "confidence": 0.73,
            "method": "keyword_based",
            "recommended_action": "Warn User"
        },
        {
            "message_id": 5,
            "message": "Thanks for helping with the project!",
            "label": "safe",
            "score": 0.96,
            "confidence": 0.96,
            "method": "advanced_model",
            "recommended_action": "Safe"
        }
    ]
    
    # Calculate summary
    toxic_count = sum(1 for r in test_results if r["label"] == "toxic")
    safe_count = len(test_results) - toxic_count
    toxicity_rate = (toxic_count / len(test_results)) * 100
    
    summary = {
        "total_messages": len(test_results),
        "toxic_messages": toxic_count,
        "safe_messages": safe_count,
        "toxicity_rate": round(toxicity_rate, 1),
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method_breakdown": {
            "advanced_model": sum(1 for r in test_results if r.get("method") == "advanced_model"),
            "keyword_based": sum(1 for r in test_results if r.get("method") == "keyword_based")
        }
    }
    
    # Store in session for export
    session['last_results'] = test_results
    session['last_summary'] = summary
    
    return render_template('results.html', results=test_results, summary=summary)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])