# SafeSpace.AI - Deployment Guide

## 🚀 Free Deployment Options

Choose your preferred deployment platform:

### 🎯 Option 1: Hugging Face Spaces (Recommended for AI Apps) ⭐
- ✅ **100% Free** forever with GPU support
- ✅ **Perfect for AI apps** with automatic model caching
- ✅ **Beautiful Gradio interface** 
- ✅ **Community visibility** and portfolio showcase
- ✅ **Zero configuration** - just upload files

### 🌐 Option 2: Render.com (Traditional Web Apps)
- ✅ Free tier with 750 hours/month
- ✅ Standard Flask deployment
- ✅ Custom domain support (paid)

---

## 🤗 Hugging Face Spaces Deployment (Recommended)

### Prerequisites
- Git repository (✅ Already created)
- GitHub account: `biswaj45` (✅ Ready)
- [Hugging Face account](https://huggingface.co) (free signup)

### Step 1: Push to GitHub
```bash
# Navigate to your project
cd "d:\Ai based Harrassment\safespace_ai"

# Add your GitHub remote  
git remote add origin https://github.com/biswaj45/safespace-ai.git

# Push to GitHub
git push -u origin master
```

### Step 2: Create Hugging Face Space
1. **Visit**: [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Fill out the form**:
   - **Owner**: Your HF username
   - **Space name**: `safespace-ai`
   - **License**: `MIT`
   - **SDK**: `Gradio` ⭐
   - **Visibility**: `Public` (recommended for portfolio)
   - **Hardware**: `CPU basic` (free)

3. **Initialize the Space** (creates empty repository)

### Step 3: Prepare Files for HF Spaces
```bash
# Clone your new HF Space (replace YOUR_HF_USERNAME)
git clone https://huggingface.co/spaces/YOUR_HF_USERNAME/safespace-ai hf-space
cd hf-space

# Copy the Gradio version of the app
cp "../app_hf.py" "./app.py"
cp "../requirements_hf.txt" "./requirements.txt"
```

### Step 4: Create HF Configuration
Create `README.md` in the HF Space directory:
```yaml
---
title: SafeSpace.AI - Workplace Harassment Detector
emoji: 🛡️
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
tags:
  - text-classification
  - workplace-safety
  - harassment-detection
  - toxicity-detection
  - ai-safety
---

# 🛡️ SafeSpace.AI - Workplace Harassment Detector

AI-powered workplace harassment detection using advanced transformers.

## ✨ Features
- 🤖 **Advanced AI**: Uses `unitary/toxic-bert` model
- 📊 **Real-time Analysis**: Instant toxicity detection  
- 📁 **File Support**: Upload .txt and .csv files
- 💾 **Export Results**: Download detailed CSV reports
- 🎨 **Modern UI**: Beautiful Gradio interface

## 🚀 How to Use
1. **Enter text** directly or **upload a file**
2. **Click Analyze** to detect toxic content
3. **Review results** with detailed recommendations
4. **Export reports** for HR documentation

## 🎯 Perfect For
- HR departments monitoring workplace communications
- Team managers assessing communication health
- Compliance officers conducting safety audits

Built with ❤️ using Hugging Face Transformers + Gradio
```

### Step 5: Deploy to HF Spaces
```bash
# Add and commit all files
git add .
git commit -m "Deploy SafeSpace.AI to Hugging Face Spaces"

# Push to deploy
git push
```

### Step 6: Access Your Live App! 🎉
- **Your app URL**: `https://huggingface.co/spaces/YOUR_USERNAME/safespace-ai`
- **Build time**: 3-5 minutes
- **First model load**: ~30 seconds

---

## 🌐 Alternative: Render.com Deployment

### Step-by-Step Deployment Instructions

#### 1. Push to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/safespace-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 2. Deploy on Render
1. Go to [https://render.com](https://render.com)
2. Sign up/Sign in with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository: `safespace-ai`
5. Configure deployment settings:
   - **Name**: `safespace-ai` (or your preferred name)
   - **Region**: Choose closest to your location
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (automatically detected from Procfile)
   - **Plan**: `Free` (0$/month)

#### 3. Environment Variables (Optional)
Set these in Render dashboard under "Environment":
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Generate a secure random string

#### 4. Deploy
- Click "Create Web Service"
- Render will automatically:
  - Clone your repository
  - Install dependencies
  - Download AI model (this may take 5-10 minutes)
  - Start the application

#### 5. Access Your App
- After successful deployment, you'll get a URL like:
  `https://safespace-ai-xyz.onrender.com`

### Expected Deployment Time
- **Initial deployment**: 8-15 minutes (downloading AI model)
- **Subsequent deployments**: 3-5 minutes

### Important Notes

#### Free Tier Limitations
- Apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 750 hours/month free usage (sufficient for demos/portfolios)

#### Model Loading
- The AI model (unitary/toxic-bert) is ~440MB
- First load on each restart takes 2-3 minutes
- Model is cached after first load

#### Performance Tips
- Keep the app "warm" by pinging it periodically
- Consider upgrading to paid plan for production use
- Monitor logs for any deployment issues

### Troubleshooting

#### If Deployment Fails
1. Check build logs in Render dashboard
2. Verify requirements.txt has all dependencies
3. Ensure Procfile exists and is correct
4. Check for Python version compatibility

#### If App Won't Start
1. Check application logs
2. Verify SECRET_KEY is set
3. Check if model download completed
4. Monitor memory usage (free tier has 512MB limit)

### File Structure Summary
```
safespace_ai/
├── app.py              # Main Flask application
├── Procfile            # Render deployment config
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── templates/          # HTML templates
│   ├── index.html      # Homepage
│   └── results.html    # Results dashboard
├── static/            # CSS and assets
│   └── style.css      # Custom styles
└── test_*.txt/csv     # Sample test files
```

### Next Steps After Deployment
1. Test all functionality on the live URL
2. Share the URL for demos/portfolio
3. Monitor usage and performance
4. Consider custom domain (paid feature)

## 🎯 Alternative: Hugging Face Spaces

If Render doesn't work, try Hugging Face Spaces:

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Create new Space
3. Choose "Gradio" or "Streamlit" 
4. Upload your files
5. Get instant URL: `https://huggingface.co/spaces/username/safespace-ai`

## 📊 Post-Deployment Testing

Test these features on your live URL:
- [ ] Homepage loads correctly
- [ ] File upload works (.txt, .csv)
- [ ] Textarea input processes messages
- [ ] Toxicity detection functions
- [ ] Results dashboard displays
- [ ] Export CSV/Summary works
- [ ] Responsive design on mobile

## 🎉 Success!

Your SafeSpace.AI app is now live and accessible worldwide!

**Live URL Format**: `https://your-app-name.onrender.com`