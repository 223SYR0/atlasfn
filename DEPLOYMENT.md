# Deployment Guide - AtlasFN on Render

This guide will help you deploy your AtlasFN website to Render.com, making it live 24/7.

## Prerequisites
- GitHub account (free at github.com)
- Render account (free at render.com)
- Your Stripe API keys

## Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click "+" → "New repository"
3. Name it `atlasfn` (or any name you prefer)
4. Create the repository

## Step 2: Push Your Project to GitHub

In PowerShell, navigate to your project folder:

```powershell
cd c:\Users\Eagle\Desktop\AtlasFN_Project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/atlasfn.git
git push -u origin main
```

(Replace YOUR_USERNAME with your actual GitHub username)

## Step 3: Deploy to Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Select "Deploy an existing Git repository"
4. Grant permission to access your GitHub repos
5. Select your `atlasfn` repository

### Configure the Web Service:

- **Name**: `atlasfn-server`
- **Environment**: `Python`
- **Region**: `Oregon` (or your preferred region)
- **Branch**: `main`
- **Build Command**: `pip install -r server/requirements.txt`
- **Start Command**: `gunicorn --chdir server server:app`
- **Plan**: `Free`

### Add Environment Variables:

Click "Advanced" and add these environment variables:

```
STRIPE_SECRET_KEY: sk_test_YOUR_SECRET_KEY
STRIPE_PUBLISHABLE_KEY: pk_test_YOUR_PUBLIC_KEY
```

(Get these from your [Stripe Dashboard](https://dashboard.stripe.com/apikeys))

4. Click "Create Web Service"

## Step 4: Wait for Deployment

Render will automatically build and deploy your app. You'll see a URL like:
```
https://atlasfn-server.onrender.com
```

## Step 5: Test Your Site

1. Visit https://atlasfn-server.onrender.com in your browser
2. Test the login, purchase flow, and payments
3. Everything should work the same as localhost

## Important Notes

- **Free tier**: Render spins down free web services after 15 minutes of inactivity
- **SSL Certificate**: Your site automatically gets HTTPS
- **24/7 Uptime**: Paid plans keep servers active 24/7
- **Updates**: Every time you push to GitHub, Render automatically redeploys

## Troubleshooting

**Server not starting?**
- Check Build Logs in Render dashboard
- Make sure requirements.txt has all dependencies

**Payment not working?**
- Verify Stripe keys are set in environment variables
- Check browser console (F12) for errors
- Ensure CSP header allows your Render domain

**Files not found?**
- The server now serves your HTML files directly
- Visit the root URL to see your main page

## Local Development

To continue developing locally:

```powershell
cd c:\Users\Eagle\Desktop\AtlasFN_Project\server
python server.py

# In another terminal:
python -m http.server 8000
# Visit http://localhost:8000
```

## Support

For Render issues: https://render.com/docs
For Stripe issues: https://stripe.com/docs
