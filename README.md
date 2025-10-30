# SafeSpace.AI - Workplace Harassment Detector

🛡️ **AI-powered workplace chat safety monitor** that detects toxic language and harassment in workplace communications using advanced machine learning.

![SafeSpace.AI](https://img.shields.io/badge/AI-Powered-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 🤖 **AI-Powered Detection**
- **Advanced Model**: Uses `unitary/toxic-bert` transformer model
- **High Accuracy**: Professional-grade toxicity detection
- **Fallback System**: Keyword-based detection as backup
- **Real-time Analysis**: Instant results for workplace safety

### 📁 **Multiple Input Methods**
- **Text Input**: Paste messages directly in textarea
- **File Upload**: Support for `.txt` and `.csv` files
- **Batch Processing**: Analyze hundreds of messages at once
- **CSV Intelligence**: Auto-detects message columns

### 📊 **Professional Dashboard**
- **Summary Statistics**: Total, toxic, safe message counts
- **Toxicity Rate**: Percentage with contextual feedback
- **Method Indicators**: Shows AI model vs keyword detection
- **Responsive Design**: Works on desktop and mobile

### 💾 **Export Capabilities**
- **Detailed CSV**: Complete analysis with all data points
- **Executive Summary**: High-level report for management
- **Timestamp Tracking**: When analysis was performed
- **Professional Format**: Ready for HR documentation

### 🎨 **Modern UI/UX**
- **Bootstrap 5**: Professional, responsive design
- **Interactive Elements**: Hover effects, loading states
- **Color Coding**: Red for toxic, green for safe
- **Mobile First**: Optimized for all screen sizes

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/safespace-ai.git
cd safespace-ai

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit: `http://localhost:5000`

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions on Render.com (free).

## 📋 How It Works

### 1. **Input Processing**
- Upload chat logs or paste messages
- Automatic file format detection
- Message parsing and validation

### 2. **AI Analysis**
- Each message analyzed individually
- Confidence scores (0-1 scale)
- Classification: TOXIC or SAFE
- Detection method tracking

### 3. **Results Dashboard**
- Visual summary with statistics
- Detailed message-by-message breakdown
- Recommended actions for each message
- Export options for documentation

### 4. **Export & Reporting**
- CSV download with full details
- Executive summary report
- Professional formatting for HR use

## 🎯 Use Cases

### **HR Departments**
- Monitor workplace chat channels
- Document harassment incidents
- Generate compliance reports
- Early intervention alerts

### **Team Managers**
- Assess team communication health
- Identify problematic patterns
- Improve workplace culture
- Preventive measures

### **Compliance Officers**
- Regular safety audits
- Policy enforcement
- Risk assessment
- Legal documentation

## 📊 Sample Results

```
Analysis Summary:
📈 5 messages analyzed
🚨 2 toxic messages (40% toxicity rate)
✅ 3 safe messages
⚠️  Needs attention

Detailed Results:
1. "Hello team!" → SAFE (0.95 confidence)
2. "You're an idiot" → TOXIC (0.87 confidence) → Warn User
3. "Great work today!" → SAFE (0.93 confidence)
```

## 🔧 Technical Stack

- **Backend**: Flask 3.0+ (Python)
- **AI Model**: unitary/toxic-bert (Hugging Face Transformers)
- **Frontend**: Bootstrap 5 + Custom CSS
- **Deployment**: Render.com (Free tier)
- **Processing**: Pandas for data handling
- **Server**: Gunicorn for production

## 📁 Project Structure

```
safespace_ai/
├── app.py                 # Main Flask application
├── Procfile              # Deployment configuration
├── requirements.txt      # Python dependencies
├── DEPLOYMENT.md         # Deployment instructions
├── templates/
│   ├── index.html        # Homepage with upload form
│   └── results.html      # Analysis results dashboard
├── static/
│   └── style.css         # Custom styling
├── test_*.txt           # Sample test files
└── README.md            # This file
```

## 🛠️ Development

### Requirements
- Python 3.8+
- Flask 3.0+
- Transformers 4.40+
- PyTorch 2.6+
- 2GB+ RAM (for AI model)

### Local Testing
```bash
# Run tests
python -m pytest

# Test with sample data
curl -X POST http://localhost:5000/analyze \
  -F "text_input=Hello team! You're stupid."

# Check exports
curl http://localhost:5000/export-csv
```

## 🎉 Demo

**Live Demo**: `https://safespace-ai.onrender.com` (after deployment)

Try these sample inputs:
- ✅ "Great job everyone, thanks for your hard work!"
- 🚨 "You're an idiot and I hate working with you"
- ✅ "Looking forward to our meeting tomorrow"
- 🚨 "This is stupid and a waste of time"

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/safespace-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/safespace-ai/discussions)
- **Email**: your-email@example.com

## 🏆 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the transformers library
- [Unitary AI](https://huggingface.co/unitary) for the toxic-bert model
- [Bootstrap](https://getbootstrap.com/) for the UI framework
- [Render](https://render.com/) for free hosting

---

**⭐ Star this repository if you find it helpful!**

**🔗 Deploy your own**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) to get your instance running in 10 minutes.