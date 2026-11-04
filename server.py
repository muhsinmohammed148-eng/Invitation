from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from functools import wraps
import time

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Data file paths
WISHES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wishes.json')

# Rate limiting: simple in-memory store
rate_limit_store = {}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 5  # max wishes per window

def check_rate_limit(ip):
    """Simple rate limiting to prevent spam."""
    now = time.time()
    if ip in rate_limit_store:
        # Clean old entries
        rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < RATE_LIMIT_WINDOW]
        if len(rate_limit_store[ip]) >= RATE_LIMIT_MAX:
            return False
    else:
        rate_limit_store[ip] = []
    rate_limit_store[ip].append(now)
    return True

def load_wishes():
    """Load wishes from JSON file."""
    if not os.path.exists(WISHES_FILE):
        return []
    try:
        with open(WISHES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []

def save_wishes(wishes):
    """Save wishes to JSON file."""
    with open(WISHES_FILE, 'w', encoding='utf-8') as f:
        json.dump(wishes, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Serve the main page."""
    return send_from_directory('.', 'index.html')

@app.route('/api/wishes', methods=['GET'])
def get_wishes():
    """Fetch all wishes."""
    wishes = load_wishes()
    # Return wishes sorted by date (newest first)
    wishes.sort(key=lambda w: w.get('createdAt', ''), reverse=True)
    return jsonify({
        'success': True,
        'count': len(wishes),
        'wishes': wishes
    })

@app.route('/api/wishes', methods=['POST'])
def add_wish():
    """Submit a new wish."""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Rate limiting check
    if not check_rate_limit(ip):
        return jsonify({
            'success': False,
            'error': 'Too many wishes. Please try again later.'
        }), 429
    
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    name = data.get('name', '').strip()
    text = data.get('text', '').strip()
    
    if not name or not text:
        return jsonify({
            'success': False,
            'error': 'Name and wish text are required'
        }), 400
    
    # Basic sanitization - limit length
    if len(name) > 100:
        name = name[:100]
    if len(text) > 1000:
        text = text[:1000]
    
    wish = {
        'id': datetime.now().isoformat(),
        'author': name,
        'text': text,
        'createdAt': datetime.now().isoformat()
    }
    
    wishes = load_wishes()
    wishes.append(wish)
    save_wishes(wishes)
    
    return jsonify({
        'success': True,
        'wish': wish
    }), 201

if __name__ == '__main__':
    # Initialize data files if they don't exist
    if not os.path.exists(WISHES_FILE):
        save_wishes([])
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
