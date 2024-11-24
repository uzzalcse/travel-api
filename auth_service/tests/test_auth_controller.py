
import pytest
import json
from flask import Flask
from flask_restx import Api
from jose import jwt
from app import app
from controllers.auth_controller import auth_namespace
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_restx")

# Secret key for JWT (same as in auth_controller.py)
SECRET_KEY = "your_secret_key"

# Generate a valid JWT token for testing
def generate_token(user_id="user123", role="User"):
    payload = {
        "user_id": user_id,
        "role": role
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app.test_client()

# Test with valid token
def test_valid_token(client):
    token = generate_token()
    response = client.post('/auth/validate', json={'token': token})
    assert response.status_code == 200
    data = response.json
    assert 'user_id' in data
    assert 'role' in data
    assert data['role'] == "User"

# Test with expired token (simulate by encoding token with a past expiration date)
def test_expired_token(client):
    expired_token = jwt.encode(
        {"user_id": "user123", "role": "User", "exp": 0},
        SECRET_KEY, algorithm="HS256"
    )
    response = client.post('/auth/validate', json={'token': expired_token})
    assert response.status_code == 401
    assert response.json['error'] == "Token has expired."

# Test with invalid token format
def test_invalid_token_format(client):
    invalid_token = "invalid_token_string"
    response = client.post('/auth/validate', json={'token': invalid_token})
    assert response.status_code == 401
    assert response.json['error'] == "Invalid token."

# Test with missing token
def test_missing_token(client):
    response = client.post('/auth/validate', json={})
    assert response.status_code == 401
    assert response.json['error'] == "Token is missing."

# Test with invalid token payload (missing 'user_id' or 'role')
def test_invalid_token_payload(client):
    # Token without 'role' in the payload
    invalid_payload_token = jwt.encode({"user_id": "user123"}, SECRET_KEY, algorithm="HS256")
    response = client.post('/auth/validate', json={'token': invalid_payload_token})
    assert response.status_code == 401
    assert response.json['error'] == "Invalid token payload."

# Test the app routing and initialization (Ensure route exists)
def test_app(client):
    response = client.get('/auth/validate')
    assert response.status_code == 405  # Method Not Allowed (GET is not allowed for /validate)
