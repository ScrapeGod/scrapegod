from functools import wraps
from flask import request, jsonify
from scrapegod.blueprints.user.models import APIKey
from scrapegod.extensions import argon2
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def validate_api_key(api_key):
    # Fetch all API keys from the database
    api_key_entries = APIKey.query.all()

    # Compare the provided API key with the hashed keys in the database
    for entry in api_key_entries:
        if argon2.check_password_hash(entry.key, api_key):
            return entry.user_id  # Return the user ID associated with the API key

    return None  # Return None if no match is found


def jwt_or_api_key_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-API-KEY") or request.args.get("api_key"):
            # If JWT fails, try API key
            print("hello")
            api_key = request.headers.get("X-API-KEY") or request.args.get("api_key")
            print(f"API key: {api_key}")
            if api_key and validate_api_key(api_key):
                return fn(current_user="api_key_user", *args, **kwargs)
            else:
                return jsonify({"msg": "Invalid API key"}), 401
        else:

            try:
                # Try JWT authentication
                verify_jwt_in_request()  # This will raise an error if JWT is not valid
                current_user = get_jwt_identity()
                return fn(current_user=current_user, *args, **kwargs)
            except Exception as e:
                print(f"JWT verification failed: {e}")
                pass

        return jsonify({"msg": "Unauthorized"}), 401

    return wrapper
