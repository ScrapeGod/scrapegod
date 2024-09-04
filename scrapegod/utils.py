from functools import wraps
from flask import request, jsonify
from scrapegod.extensions import db


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        VALID_API_KEYS = []
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key not in VALID_API_KEYS:
            return jsonify({'message': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function