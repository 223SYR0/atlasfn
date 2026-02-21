# Payment Backend Server

This is a Flask backend server for processing Stripe payments.

## Setup

1. **Install dependencies** (already done):
   ```
   pip install -r requirements.txt
   ```

2. **Get your Stripe API keys**:
   - Go to https://dashboard.stripe.com/apikeys
   - Copy your **Secret Key** (starts with `sk_test_` or `sk_live_`)
   - Copy your **Public Key** (starts with `pk_test_` or `pk_live_`)

3. **Add your keys to `.env` file**:
   - Open `.env` in this folder
   - Replace `sk_test_YOUR_SECRET_KEY_HERE` with your actual secret key
   - Replace `pk_test_YOUR_PUBLIC_KEY_HERE` with your actual public key

4. **Run the server**:
   ```
   python server.py
   ```
   
   You should see:
   ```
   🚀 Server starting on http://localhost:3000
   ```

## Testing

- Server health check: http://localhost:3000/health
- Main endpoint: http://localhost:3000/

## How it works

The HTML file (test.html) connects to this server at `http://localhost:3000` to:
1. Create a Stripe Payment Intent
2. Process donations
3. Handle payment confirmations

The server is already configured in your HTML file to use localhost:3000.

## Important

- Keep your `.env` file private (don't commit to GitHub)
- Never expose your secret key in the HTML file
- Only use test keys for development
- Switch to live keys when in production
