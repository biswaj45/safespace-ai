import gradio as gr
import pandas as pd
from transformers import pipeline
import io
import csv
from datetime import datetime
import tempfile
import os

# Initialize the toxicity detection pipeline
print("Loading AI model for toxicity detection...")
try:
    classifier = pipeline(
        "text-classification",
        model="unitary/toxic-bert",
        tokenizer="unitary/toxic-bert"
    )
    model_loaded = True
    print("✅ AI model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load AI model: {e}")
    classifier = None
    model_loaded = False

# Fallback keyword detection
TOXIC_KEYWORDS = [
    'hate', 'stupid', 'idiot', 'loser', 'pathetic', 'worthless', 'useless',
    'shut up', 'go away', 'get lost', 'moron', 'dumb', 'fool', 'jerk'
]

def classify_toxicity(text):
    """Classify a single message for toxicity"""
    if not text or not text.strip():
        return "SAFE", 0.1, "Empty message"
    
    text = text.strip()
    
    # Try AI model first
    if model_loaded and classifier:
        try:
            result = classifier(text)
            if isinstance(result, list) and len(result) > 0:
                prediction = result[0]
                label = prediction.get('label', 'SAFE')
                confidence = prediction.get('score', 0.5)
                
                # Convert labels to our format
                if label in ['TOXIC', 'toxic', '1']:
                    return "TOXIC", confidence, "AI Model"
                else:
                    return "SAFE", confidence, "AI Model"
        except Exception as e:
            print(f"AI model error: {e}")
    
    # Fallback to keyword detection
    text_lower = text.lower()
    for keyword in TOXIC_KEYWORDS:
        if keyword in text_lower:
            return "TOXIC", 0.7, "Keyword Detection"
    
    return "SAFE", 0.8, "Keyword Detection"

def analyze_text(text_input):
    """Analyze text input from the textarea"""
    if not text_input:
        return "Please enter some text to analyze.", None, None
    
    messages = [line.strip() for line in text_input.split('\n') if line.strip()]
    if not messages:
        return "No valid messages found.", None, None
    
    results = []
    toxic_count = 0
    
    for i, message in enumerate(messages, 1):
        classification, confidence, method = classify_toxicity(message)
        
        if classification == "TOXIC":
            toxic_count += 1
            action = "⚠️ Review Needed"
            color = "🔴"
        else:
            action = "✅ No Action"
            color = "🟢"
        
        results.append({
            'Message #': i,
            'Message': message[:100] + "..." if len(message) > 100 else message,
            'Classification': f"{color} {classification}",
            'Confidence': f"{confidence:.2f}",
            'Method': method,
            'Action': action
        })
    
    total_messages = len(messages)
    safe_count = total_messages - toxic_count
    toxicity_rate = (toxic_count / total_messages) * 100
    
    # Create summary
    summary = f"""
## 📊 Analysis Summary
- **Total Messages**: {total_messages}
- **🚨 Toxic Messages**: {toxic_count} ({toxicity_rate:.1f}%)
- **✅ Safe Messages**: {safe_count} ({100-toxicity_rate:.1f}%)
- **🤖 AI Model Status**: {'✅ Active' if model_loaded else '⚠️ Using Keywords'}

### 📋 Recommendations:
"""
    
    if toxicity_rate > 30:
        summary += "🚨 **High Risk**: Immediate HR intervention recommended"
    elif toxicity_rate > 10:
        summary += "⚠️ **Medium Risk**: Monitor closely and provide training"
    elif toxicity_rate > 0:
        summary += "🟡 **Low Risk**: Minor issues detected, consider informal discussion"
    else:
        summary += "✅ **Healthy Communication**: No toxic content detected"
    
    # Convert results to DataFrame for display
    df = pd.DataFrame(results)
    
    return summary, df, results

def analyze_file(file):
    """Analyze uploaded file"""
    if file is None:
        return "Please upload a file.", None, None
    
    try:
        # Read file content
        if file.name.endswith('.csv'):
            df = pd.read_csv(file.name)
            # Try to find message column
            message_columns = ['message', 'text', 'content', 'chat', 'comment']
            message_col = None
            
            for col in df.columns:
                if col.lower() in message_columns:
                    message_col = col
                    break
            
            if message_col is None:
                message_col = df.columns[0]  # Use first column
            
            messages = df[message_col].dropna().astype(str).tolist()
        else:
            # Assume text file
            with open(file.name, 'r', encoding='utf-8') as f:
                content = f.read()
            messages = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not messages:
            return "No messages found in the file.", None, None
        
        # Join messages and analyze
        text_input = '\n'.join(messages)
        return analyze_text(text_input)
        
    except Exception as e:
        return f"Error processing file: {str(e)}", None, None

def export_results(results_data):
    """Export results to CSV"""
    if not results_data:
        return None
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
    
    try:
        writer = csv.writer(temp_file)
        # Write header
        if results_data:
            writer.writerow(results_data[0].keys())
            # Write data
            for row in results_data:
                writer.writerow(row.values())
        
        temp_file.close()
        return temp_file.name
    except Exception as e:
        return None

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="SafeSpace.AI - Workplace Harassment Detector", theme=gr.themes.Soft()) as app:
        
        # Header
        gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
            <h1>🛡️ SafeSpace.AI</h1>
            <h3>Workplace Harassment Detector</h3>
            <p>AI-powered toxicity detection for safer workplace communications</p>
        </div>
        """)
        
        # Description
        gr.Markdown("""
        ### 🎯 How it works:
        1. **Upload a file** (.txt or .csv) or **paste text** directly
        2. **AI analyzes** each message for toxic content
        3. **Get detailed results** with recommendations
        4. **Export reports** for HR documentation
        
        *Uses advanced AI (unitary/toxic-bert) with keyword fallback for maximum accuracy.*
        """)
        
        # Input methods
        with gr.Tab("📝 Text Input"):
            text_input = gr.Textbox(
                label="Paste your messages here (one per line)",
                placeholder="Enter workplace messages to analyze...\nExample:\nHello team, great work today!\nYou're an idiot and I hate working with you.\nLooking forward to our meeting.",
                lines=8
            )
            text_button = gr.Button("🔍 Analyze Text", variant="primary")
        
        with gr.Tab("📁 File Upload"):
            file_input = gr.File(
                label="Upload chat log file (.txt or .csv)",
                file_types=[".txt", ".csv"]
            )
            file_button = gr.Button("🔍 Analyze File", variant="primary")
        
        # Results section
        with gr.Row():
            with gr.Column():
                summary_output = gr.Markdown(label="📊 Analysis Summary")
            
        results_table = gr.Dataframe(
            label="📋 Detailed Results",
            interactive=False
        )
        
        # Export section
        with gr.Row():
            export_button = gr.Button("💾 Export Results (CSV)", variant="secondary")
            download_file = gr.File(label="📥 Download Results", visible=False)
        
        # Store results for export
        results_state = gr.State(value=None)
        
        # Event handlers
        def handle_text_analysis(text):
            summary, df, results = analyze_text(text)
            return summary, df, results
        
        def handle_file_analysis(file):
            summary, df, results = analyze_file(file)
            return summary, df, results
        
        def handle_export(results_data):
            if results_data:
                file_path = export_results(results_data)
                return gr.File(value=file_path, visible=True)
            return gr.File(visible=False)
        
        # Connect events
        text_button.click(
            fn=handle_text_analysis,
            inputs=[text_input],
            outputs=[summary_output, results_table, results_state]
        )
        
        file_button.click(
            fn=handle_file_analysis,
            inputs=[file_input],
            outputs=[summary_output, results_table, results_state]
        )
        
        export_button.click(
            fn=handle_export,
            inputs=[results_state],
            outputs=[download_file]
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid #eee;">
            <p>🛡️ <strong>SafeSpace.AI</strong> - Built with Flask + Hugging Face Transformers</p>
            <p>🔒 Your data is processed securely and not stored</p>
        </div>
        """)
    
    return app

# Create and launch the app
if __name__ == "__main__":
    app = create_interface()
    app.launch()