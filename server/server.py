from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import secrets

load_dotenv()

# Get the parent directory for static files
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '..')
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

# Security: Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:*",
            "http://127.0.0.1:*",
            "https://*.onrender.com",
            "https://*.github.io",
            "https://*.netlify.app",
            "https://atlasfn.com"
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

# Security: Rate limiting storage
rate_limit_storage = {}

# Security: Rate limiting decorator
def rate_limit(max_requests=10, window_seconds=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = datetime.now()
            
            # Clean old entries
            if client_ip in rate_limit_storage:
                rate_limit_storage[client_ip] = [
                    req_time for req_time in rate_limit_storage[client_ip]
                    if now - req_time < timedelta(seconds=window_seconds)
                ]
            else:
                rate_limit_storage[client_ip] = []
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Set your Stripe secret key here
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_YOUR_SECRET_KEY_HERE')

# Security: Validate request origin
def validate_origin():
    origin = request.headers.get('Origin', '')
    allowed_origins = ['http://localhost', 'https://localhost', 'file://']
    return any(origin.startswith(allowed) for allowed in allowed_origins)

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/', methods=['GET'])
def serve_home():
    """Serve main HTML file"""
    return send_from_directory(STATIC_FOLDER, 'ballsackblud.html')

@app.route('/login', methods=['GET'])
def serve_login():
    """Serve login page"""
    return send_from_directory(STATIC_FOLDER, 'login.html')

@app.route('/signup', methods=['GET'])
def serve_signup():
    """Serve signup page"""
    return send_from_directory(STATIC_FOLDER, 'signup.html')

@app.route('/settings', methods=['GET'])
def serve_settings():
    """Serve settings page"""
    return send_from_directory(STATIC_FOLDER, 'settings.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    """Serve any static files (images, etc)"""
    return send_from_directory(STATIC_FOLDER, filename)

@app.route('/create-payment-intent', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=60)
def create_payment_intent():
    try:
        data = request.json
        
        # Security: Validate JSON data exists
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        # Security: Validate amount
        amount = data.get('amount')
        if not amount or not isinstance(amount, (int, float)):
            return jsonify({'error': 'Invalid amount'}), 400
            
        if amount < 100:  # $1 minimum
            return jsonify({'error': 'Minimum amount is $1.00'}), 400
            
        if amount > 1000000:  # $10,000 maximum
            return jsonify({'error': 'Maximum amount is $10,000'}), 400
        
        # Security: Validate email format
        email = data.get('email', '')
        if not email or '@' not in email or len(email) > 254:
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Security: Sanitize name
        name = data.get('name', '')[:100]  # Limit length
        if not name or len(name) < 2:
            return jsonify({'error': 'Please provide a valid name'}), 400
        
        # Security: Validate phone (optional but recommended)
        phone = data.get('phone', '')[:50]
        
        # Security: Validate address
        address = data.get('address', {})
        if not isinstance(address, dict):
            return jsonify({'error': 'Invalid address format'}), 400
            
        address_line1 = address.get('line1', '')[:200]
        address_city = address.get('city', '')[:100]
        address_state = address.get('state', '')[:50]
        address_postal_code = address.get('postal_code', '')[:20]
        address_country = address.get('country', 'US')[:2]
        
        # Validate required address fields
        if not address_line1:
            return jsonify({'error': 'Street address is required'}), 400
        if not address_city:
            return jsonify({'error': 'City is required'}), 400
        if not address_postal_code:
            return jsonify({'error': 'Zip/postal code is required'}), 400
        
        # Security: Generate idempotency key
        idempotency_key = secrets.token_urlsafe(32)
        
        # Create payment intent with security measures and full billing details
        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='usd',
            metadata={
                'email': email,
                'name': name,
                'phone': phone,
                'address': f"{address_line1}, {address_city}, {address_state} {address_postal_code}",
                'country': address_country,
                'timestamp': datetime.now().isoformat()
            },
            idempotency_key=idempotency_key,
            description=f'Donation from {name} ({email})',
            receipt_email=email
        )
        
        app.logger.info(f'Payment intent created: {intent.id} for ${amount/100:.2f}')
        
        return jsonify({
            'clientSecret': intent.client_secret
        })
        
    except stripe.error.CardError as e:
        return jsonify({'error': f'Card error: {e.user_message}'}), 400
    except stripe.error.RateLimitError:
        return jsonify({'error': 'Too many requests. Please try again later.'}), 429
    except stripe.error.InvalidRequestError as e:
        return jsonify({'error': f'Invalid request: {str(e)}'}), 400
    except stripe.error.AuthenticationError:
        return jsonify({'error': 'Authentication with Stripe failed'}), 500
    except stripe.error.StripeError as e:
        return jsonify({'error': 'Payment service error. Please try again.'}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'Server is running'}), 200

if __name__ == '__main__':
    import logging
    
    # Security: Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Security warnings
    if not os.getenv('STRIPE_SECRET_KEY') or os.getenv('STRIPE_SECRET_KEY') == 'sk_test_YOUR_SECRET_KEY_HERE':
        app.logger.warning('⚠️  WARNING: Using default Stripe key. Set STRIPE_SECRET_KEY in .env file')
    
    print('=' * 60)
    print('🚀 Atlasfn Payment Server Starting')
    print('=' * 60)
    print('🔒 Security Features Enabled:')
    print('  ✅ CORS Protection')
    print('  ✅ Rate Limiting (5 requests/minute)')
    print('  ✅ Input Validation')
    print('  ✅ Security Headers')
    print('  ✅ Error Handling')
    print('=' * 60)
    print('⚠️  Remember: Use HTTPS in production!')
    print('=' * 60)
    
    # Get PORT from environment variable (Render/Heroku) or default to 3000
    port = int(os.getenv('PORT', 3000))
    
    # Run in development mode
    # IMPORTANT: In production, use a production WSGI server like gunicorn
    app.run(debug=False, port=port, host='0.0.0.0')
