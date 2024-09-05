from functools import wraps
from flask import request, jsonify
from scrapegod.blueprints.user.models import APIKey
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def validate_api_key(api_key):
    VALID_API_KEYS = [api_key.key for api_key in APIKey.query.all()]

    return api_key in VALID_API_KEYS


def jwt_or_api_key_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-API-KEY") or request.args.get("api_key"):
            # If JWT fails, try API key
            api_key = request.headers.get("X-API-KEY") or request.args.get("api_key")
            if api_key and validate_api_key(api_key):
                return fn(current_user="api_key_user", *args, **kwargs)
        else:

            try:
                # Try JWT authentication
                verify_jwt_in_request()  # This will raise an error if JWT is not valid
                current_user = get_jwt_identity()
                return fn(current_user=current_user, *args, **kwargs)
            except:
                pass

        return jsonify({"msg": "Unauthorized"}), 401

    return wrapper
