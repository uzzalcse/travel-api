import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from user_service.services.user_service import login_user
from auth_service.utils.decorators import SECRET_KEY  # The shared secret key for JWT encoding

def login():
    """
    Handles user login and generates a JWT token.
    """
    try:
        data = request.json
        token = login_user(data)  # Get the token after validating user login
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


def validate_token():
    """
    Validates the JWT token in the request header.
    """
    try:
        token = request.headers.get('Authorization').split()[1]  # Get token from Authorization header
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Add user_id and role to request context for role-based access control
        request.user_id = decoded["user_id"]
        request.role = decoded["role"]

        return True  # Token is valid
    except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        return jsonify({"error": "Invalid or expired token"}), 401


def role_required(role):
    """
    Decorator that checks if the user has the correct role (Admin or User).
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            if request.role != role:
                return jsonify({"error": "Access forbidden: insufficient role"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
