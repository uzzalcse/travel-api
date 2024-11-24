import pytest
from flask import Flask
from controllers.user_controller import app, USERS, SECRET_KEY
from utils.password_utils import hash_password
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_register_user(client):
    """Test user registration endpoint"""
    USERS.clear()  # Clear existing mock data
    data = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123",
        "role": "User"
    }
    response = client.post("/user/register", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Alice"
    assert len(USERS) == 1
    assert USERS[0]["email"] == "alice@example.com"


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    USERS.clear()  # Clear existing mock data
    USERS.append({
        "id": "user-123",
        "name": "Existing User",
        "email": "existing@example.com",
        "password": hash_password("password123"),
        "role": "User"
    })
    data = {
        "name": "New User",
        "email": "existing@example.com",
        "password": "password123",
    }
    response = client.post("/user/register", json=data)
    assert response.status_code == 400
    assert "Email already registered" in response.json["error"]


def test_login_success(client):
    """Test login with valid credentials"""
    USERS.clear()  # Clear existing mock data
    USERS.append({
        "id": "user-123",
        "name": "Test User",
        "email": "test@example.com",
        "password": hash_password("testpassword"),
        "role": "User"
    })
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/user/login", json=data)
    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/user/login", json=data)
    assert response.status_code == 400
    assert "Invalid email or password" in response.json["error"]


@patch("controllers.user_controller.jwt.decode")
def test_get_profile_success(mock_jwt_decode, client):
    """Test profile retrieval with valid token"""
    USERS.clear()  # Clear existing mock data
    USERS.append({
        "id": "user-123",
        "name": "Test User",
        "email": "test@example.com",
        "password": hash_password("testpassword"),
        "role": "User"
    })

    # Mock JWT decode
    mock_jwt_decode.return_value = {
        "user_id": "user-123",
        "role": "User",
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()
    }

    headers = {"Authorization": "Bearer mocktoken"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    assert response.json["name"] == "Test User"
    assert response.json["email"] == "test@example.com"


def test_get_profile_unauthorized(client):
    """Test profile retrieval without token"""
    response = client.get("/user/profile")
    assert response.status_code == 401
    assert "Token is missing." in response.json["message"]
