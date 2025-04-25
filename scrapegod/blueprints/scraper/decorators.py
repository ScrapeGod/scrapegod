from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from scrapegod.blueprints.user.models import User  # Adjust the import path as needed

def role_required(*roles):
    """
    Decorator to restrict access to users with specific roles.
    :param roles: List of roles allowed to access the route.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()  # Assuming you're using Flask-JWT-Extended
            user = User.query.get(current_user_id)
            if not user or user.role not in roles:
                return jsonify({'error': 'Access forbidden: insufficient permissions'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator