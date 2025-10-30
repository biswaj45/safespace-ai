# SafeSpace.AI - Deployment Guide

## 🚀 Free Deployment on Render

Follow these steps to deploy SafeSpace.AI for free on Render.com:

### Prerequisites
- Git repository (✅ Already created)
- GitHub account 
- Render.com account (free)

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