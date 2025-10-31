from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session, g
from functools import wraps
import os
import csv
from io import StringIO
from datetime import datetime
import hashlib
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not available - using system environment variables")

# Skip PyTorch for this lightweight test
AI_AVAILABLE = False
print("🚀 Running in lightweight mode - Groq API only")

# Configuration for explanation caching
EXPLANATION_CACHE = {}
EXPLANATION_CACHE_FILE = 'explanation_cache.json'

# Configuration for rewrite caching
REWRITE_CACHE = {}
REWRITE_CACHE_FILE = 'rewrite_cache.json'

# Load explanation cache from file if it exists
try:
    if os.path.exists(EXPLANATION_CACHE_FILE):
        with open(EXPLANATION_CACHE_FILE, 'r') as f:
            EXPLANATION_CACHE = json.load(f)
        print(f"📝 Loaded {len(EXPLANATION_CACHE)} cached explanations")
except Exception as e:
    print(f"⚠️ Could not load explanation cache: {e}")

# Load rewrite cache from file if it exists  
try:
    if os.path.exists(REWRITE_CACHE_FILE):
        with open(REWRITE_CACHE_FILE, 'r') as f:
            REWRITE_CACHE = json.load(f)
        print(f"✏️ Loaded {len(REWRITE_CACHE)} cached rewrites")
except Exception as e:
    print(f"⚠️ Could not load rewrite cache: {e}")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# API Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

if GROQ_API_KEY:
    print("🌐 API MODE: Using Groq API for ultra-fast detection")
    print("⚡ No model downloads - instant startup!")
else:
    print("⚠️ No Groq API key - using rule-based detection only")

def call_groq_api(text, task="toxicity"):
    """Call Groq API for ultra-fast toxicity detection or rewriting"""
    import requests
    
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
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
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
                        'source': 'groq'
                    }
                elif answer.startswith('SAFE:'):
                    reason = answer[5:].strip()
                    return {
                        'is_toxic': False,
                        'confidence': 0.95,
                        'reason': reason,
                        'source': 'groq'
                    }
                
        elif task == "rewrite":
            # Simple empathetic rewriting prompt for mixed content
            system_prompt = """Rewrite this message by keeping any good/constructive parts and only replacing toxic/profane words with respectful alternatives. Keep the same structure and meaning.

Examples:
- "I am doing good. but you are behaving as shit." → "I am doing good. but I'm concerned about your behavior."
- "Thank you, but you're being an idiot" → "Thank you, but I disagree with your approach"
- "Hello, you fucking moron" → "Hello, I have some concerns"

Respond with only the rewritten message."""

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Rewrite: '{text}'"}
                ],
                "max_tokens": 100,
                "temperature": 0.3
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                rewritten = result['choices'][0]['message']['content'].strip()
                
                # Clean up the response
                rewritten = rewritten.strip('"').strip()
                
                # Basic quality check
                if len(rewritten) > 5 and rewritten.lower() != text.lower():
                    return rewritten
                    
    except Exception as e:
        print(f"🔴 Groq API error: {e}")
        return None
    
    return None

def classify_message_toxicity(text):
    """Simple API-only classification using Groq"""
    
    # Use Groq API for all classifications
    if GROQ_API_KEY:
        api_result = call_groq_api(text, "toxicity")
        if api_result:
            print(f"🟢 Groq API classified: {api_result['source']}")
            return api_result
        else:
            print("🔴 Groq API failed - returning safe default")
            return {
                'is_toxic': False,
                'confidence': 0.5,
                'reason': "API unavailable - default safe classification",
                'source': 'fallback'
            }
    else:
        print("🔴 No API key - returning safe default")
        return {
            'is_toxic': False,
            'confidence': 0.5,
            'reason': "No API key configured - default safe classification",
            'source': 'fallback'
        }
    
    # Step 4: Default safe for unclear cases
    return {
        'is_toxic': False,
        'confidence': 0.5,
        'reason': "Unable to determine toxicity clearly",
        'source': 'default'
    }

def generate_empathy_rewrite(text):
    """Generate smart empathetic rewrite using Groq API"""
    
    # Simple check: if message has constructive indicators, proceed with rewrite
    constructive_indicators = ['i am', 'i\'m', 'doing good', 'doing well', 'thank you', 'thanks', 
                              'hello', 'hi', 'hey', 'appreciate', 'help', 'but', 'however', 'while']
    
    text_lower = text.lower()
    has_constructive_content = any(indicator in text_lower for indicator in constructive_indicators)
    
    if not has_constructive_content:
        print("🚫 No rewrite needed - purely derogatory with no constructive content")
        return None
    
    # Skip cache for fresh results - directly call API every time
    print("� Generating fresh empathetic rewrite with Groq (no cache)")
    
    # Try Groq API
    if GROQ_API_KEY:
        rewrite = call_groq_api(text, "rewrite")
        if rewrite:
            if rewrite.strip() == "NO_REWRITE_NEEDED" or "NO_REWRITE_NEEDED" in rewrite:
                print("🚫 No rewrite needed - message is purely derogatory")
                return None
            else:
                print("✅ Generated fresh empathetic rewrite with Groq")
                return rewrite
    
    # Fallback: return None for purely derogatory messages
    return None

def save_rewrite_cache():
    """Save rewrite cache to file"""
    try:
        with open(REWRITE_CACHE_FILE, 'w') as f:
            json.dump(REWRITE_CACHE, f, indent=2)
    except Exception as e:
        print(f"⚠️ Could not save rewrite cache: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Debug: Print request info
        print(f"🔍 Request method: {request.method}")
        print(f"🔍 Content type: {request.content_type}")
        print(f"🔍 Raw data: {request.get_data()}")
        
        # Try different ways to get the data
        data = None
        message = None
        
        # Check for file upload first
        if 'file_upload' in request.files:
            uploaded_file = request.files['file_upload']
            if uploaded_file and uploaded_file.filename:
                print(f"🔍 File uploaded: {uploaded_file.filename}")
                try:
                    # Read file content
                    file_content = uploaded_file.read().decode('utf-8')
                    message = file_content.strip()
                    print(f"🔍 File content length: {len(message)} characters")
                except Exception as e:
                    return jsonify({'error': f'Could not read file: {str(e)}'}), 400
        
        # If no file or file is empty, try form data
        if not message:
            if request.content_type == 'application/json':
                data = request.get_json()
            else:
                # Try form data
                data = request.form.to_dict()
                if not data:
                    # Try raw JSON parsing
                    try:
                        import json
                        data = json.loads(request.get_data().decode('utf-8'))
                    except:
                        pass
            
            print(f"🔍 Parsed data: {data}")
            
            # Check for message in multiple field names
            if data:
                message = data.get('message') or data.get('text') or data.get('text_input')
        
        if not message:
            return jsonify({'error': 'No message provided', 'debug': f'data={data}'}), 400
        
        message = message.strip()
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        print(f"🔍 Analyzing: '{message}'")
        
        # Classify the message
        result = classify_message_toxicity(message)
        
        # Prepare response
        response = {
            'is_toxic': result['is_toxic'],
            'confidence': result['confidence'],
            'score': result['confidence'],  # Frontend expects 'score'
            'explanation': result['reason'],
            'source': result['source'],
            'status': 'toxic' if result['is_toxic'] else 'safe',  # Frontend compatibility
            'label': 'toxic' if result['is_toxic'] else 'safe'   # Frontend expects 'label'
        }
        
        # Generate rewrite if toxic
        if result['is_toxic']:
            rewrite = generate_empathy_rewrite(message)
            if rewrite:  # Only include rewrite if it's not None
                response['rewrite'] = rewrite  # Frontend expects 'rewrite'
                response['empathy_rewrite'] = rewrite  # Keep for backward compatibility
                response['suggestion'] = rewrite  # Keep for backward compatibility
        
        print(f"📊 Result: {'TOXIC' if result['is_toxic'] else 'SAFE'} ({result['confidence']:.1%}) via {result['source']}")
        
        # Debug: Print the exact response being sent
        print(f"🔍 Response being sent: {response}")
        
        # For bulk analysis, render HTML template instead of returning JSON
        analysis_results = [{
            'message_id': 1,
            'message': message,
            'is_toxic': result['is_toxic'],
            'label': 'toxic' if result['is_toxic'] else 'safe',
            'confidence': result['confidence'],
            'score': result['confidence'],  # Template expects 'score'
            'explanation': result['reason'],
            'source': result['source'],
            'rewrite': response.get('rewrite', ''),
            'empathy_rewrite': response.get('rewrite', ''),
            'method': 'Groq API',
            'recommended_action': 'Review and Address' if result['is_toxic'] else 'No Action Needed',
            'rewrite_reason': 'AI-generated empathetic alternative' if response.get('rewrite') else '',
            'rewrite_type': 'rewrite' if response.get('rewrite') else ''
        }]
        
        # Create summary object that the template expects
        from datetime import datetime
        toxic_count = 1 if result['is_toxic'] else 0
        safe_count = 0 if result['is_toxic'] else 1
        total_count = 1
        
        summary = {
            'total_messages': total_count,
            'toxic_messages': toxic_count,
            'safe_messages': safe_count,
            'toxicity_rate': round((toxic_count / total_count) * 100, 1) if total_count > 0 else 0,
            'total_cleaned': 1 if result['is_toxic'] and response.get('rewrite') else 0,
            'removed_count': 0,
            'rewrites_count': 1 if result['is_toxic'] and response.get('rewrite') else 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return render_template('results.html', 
                             results=analysis_results,
                             summary=summary)
        
    except Exception as e:
        print(f"❌ Error in analyze: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Analysis failed', 'details': str(e)}), 500

@app.route('/api/analyze-realtime', methods=['POST'])
def analyze_realtime():
    """Real-time analysis endpoint for frontend compatibility"""
    return analyze()

if __name__ == '__main__':
    print("🚀 Starting SafeSpace.AI (Groq-powered)...")
    port = int(os.environ.get('PORT', 7860))  # Use 7860 for Hugging Face Spaces
    app.run(host='0.0.0.0', port=port, debug=False)