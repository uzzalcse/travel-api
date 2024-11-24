
import warnings

import pytest
from flask import Flask
from flask_restx import Api
from controllers.destination_controller import destination_namespace
from app import app as flask_app
from jose import jwt
import uuid

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_restx")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="jsonschema")




# Set up a mock valid JWT token
def create_jwt_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role
    }
    return jwt.encode(payload, "your_secret_key", algorithm="HS256")


@pytest.fixture
def app():
    """Fixture to set up the Flask app for testing."""
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Fixture to create a test client."""
    return app.test_client()


# Test for GET /destination
def test_get_destinations_valid_token(client):
    token = create_jwt_token(user_id="user1", role="Admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/destination", headers=headers)
    
    assert response.status_code == 200
    assert len(response.json) > 0  # Ensure there are destinations returned


def test_get_destinations_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/destination", headers=headers)
    
    assert response.status_code == 401
    assert response.json.get("error") == "Token has expired" or "Invalid token"


def test_get_destinations_missing_token(client):
    response = client.get("/destination")
    
    assert response.status_code == 401
    assert response.json.get("error") == "Token is missing or invalid."


# Test for POST /destination
def test_create_destination_valid_token(client):
    token = create_jwt_token(user_id="user1", role="Admin")
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "name": "New York",
        "description": "The Big Apple"
    }
    
    response = client.post("/destination", json=data, headers=headers)
    
    assert response.status_code == 201
    assert response.json["name"] == "New York"
    assert response.json["description"] == "The Big Apple"


def test_create_destination_invalid_token(client):
    token = create_jwt_token(user_id="user1", role="Admin")
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "name": "New York",
        "description": "The Big Apple"
    }
    
    # Making the user role non-admin
    token = create_jwt_token(user_id="user1", role="User")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/destination", json=data, headers=headers)
    
    assert response.status_code == 403
    assert response.json["error"] == "Forbidden: Only Admins can create destinations."


def test_create_destination_missing_token(client):
    data = {
        "name": "New York",
        "description": "The Big Apple"
    }
    
    response = client.post("/destination", json=data)
    
    assert response.status_code == 401
    assert response.json.get("error") == "Token is missing or invalid."


# Test for DELETE /destination/{id}
def test_delete_destination_valid_token(client):
    # Create a destination to delete
    token = create_jwt_token(user_id="user1", role="Admin")
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "name": "Los Angeles",
        "description": "The City of Angels"
    }
    
    post_response = client.post("/destination", json=data, headers=headers)
    destination_id = post_response.json["id"]
    
    # Now test delete
    delete_response = client.delete(f"/destination/{destination_id}", headers=headers)
    
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == f"Destination 'Los Angeles' deleted successfully."


def test_delete_destination_invalid_token(client):
    destination_id = str(uuid.uuid4())
    response = client.delete(f"/destination/{destination_id}", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == 401
    assert response.json.get("error") == "Token has expired" or "Invalid token"


def test_delete_destination_missing_token(client):
    destination_id = str(uuid.uuid4())
    response = client.delete(f"/destination/{destination_id}")
    
    assert response.status_code == 401
    assert response.json.get("error") == "Token is missing or invalid."


def test_delete_destination_non_existing(client):
    token = create_jwt_token(user_id="user1", role="Admin")
    response = client.delete(f"/destination/{str(uuid.uuid4())}", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 404
    assert response.json["error"] == "Destination not found"
