

from flask import request
from flask_restx import Namespace, Resource, fields
from jose import jwt
import uuid  # Import the uuid module to generate unique IDs

# Secret key for JWT (shared across services for token validation)
SECRET_KEY = "your_secret_key"

# Define the Namespace for "Destination Management"
destination_namespace = Namespace("destination", description="Destination Management Operations")

# Define the data model for a Destination (used for Swagger documentation)
destination_model = destination_namespace.model(
    "Destination",
    {
        "id": fields.String(description="Destination ID"),  # Unique identifier
        "name": fields.String(required=True, description="Destination Name"),  # Name of the destination
        "description": fields.String(required=True, description="Description of the Destination"),  # Description field
    },
)

# Define a model for creating a new destination
create_destination_model = destination_namespace.model(
    "CreateDestination",
    {
        "name": fields.String(required=True, description="Destination Name"),  # Required name field
        "description": fields.String(required=True, description="Description of the Destination"),  # Required description field
    },
)

# Define a general response model
response_model = destination_namespace.model(
    "Response",
    {
        "message": fields.String(description="Response Message"),  # Success or error message
    },
)

# Mocked destination data for simplicity (to replace with database in production)
DESTINATIONS = [
    {"id": str(uuid.uuid4()), "name": "Paris", "description": "The City of Light"},
    {"id": str(uuid.uuid4()), "name": "Tokyo", "description": "The Land of the Rising Sun"},
]

# Helper function to validate JWT tokens and extract user information
def validate_token(token):
    """
    Validate and decode a JWT token.

    Args:
        token (str): The token to validate.

    Returns:
        dict: User information including user_id and role.

    Raises:
        ValueError: If the token is invalid or expired.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")
        role = decoded.get("role")
        if not user_id or not role:
            raise jwt.JWTError("Invalid token payload")
        return {"user_id": user_id, "role": role}
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.JWTError:
        raise ValueError("Invalid token")

# **GET** Endpoint: Retrieve all destinations
@destination_namespace.route("")
class ManageDestinations(Resource):
    @destination_namespace.response(200, "Destinations retrieved successfully", fields.List(fields.Nested(destination_model)))
    @destination_namespace.response(401, "Unauthorized: Invalid or missing token")
    def get(self):
        """
        Retrieve a list of all travel destinations.
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Token is missing or invalid."}, 401

        token = auth_header.split(" ")[1]
        try:
            validate_token(token)  # Validate the token
        except ValueError as e:
            return {"error": str(e)}, 401

        return DESTINATIONS, 200  # Return the list of destinations

    # **POST** Endpoint: Create a new destination (Admin-only)
    @destination_namespace.response(201, "Destination created successfully", destination_model)
    @destination_namespace.response(403, "Forbidden: Only Admins can create destinations")
    @destination_namespace.response(401, "Unauthorized: Invalid or missing token")
    @destination_namespace.expect(create_destination_model)  # Expect a JSON body
    def post(self):
        """
        Create a new travel destination (Admin-only).
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Token is missing or invalid."}, 401

        token = auth_header.split(" ")[1]
        try:
            user = validate_token(token)  # Validate the token
        except ValueError as e:
            return {"error": str(e)}, 401

        # Check if the user is an Admin
        if user["role"] != "Admin":
            return {"error": "Forbidden: Only Admins can create destinations."}, 403

        # Parse and validate the request body
        data = request.json
        new_destination = {
            "id": str(uuid.uuid4()),  # Generate a unique UUID for the destination
            "name": data["name"],
            "description": data["description"],
        }
        DESTINATIONS.append(new_destination)  # Add the destination
        print(DESTINATIONS)
        return new_destination, 201

# **DELETE** Endpoint: Delete a specific destination (Admin-only)
@destination_namespace.route("/<string:id>")
class DeleteDestination(Resource):
    @destination_namespace.response(200, "Destination deleted successfully", response_model)
    @destination_namespace.response(403, "Forbidden: Only Admins can delete destinations")
    @destination_namespace.response(404, "Destination not found")
    @destination_namespace.response(401, "Unauthorized: Invalid or missing token")
    def delete(self, id):
        """
        Delete a specific travel destination (Admin-only).
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Token is missing or invalid."}, 401

        token = auth_header.split(" ")[1]
        try:
            user = validate_token(token)  # Validate the token
        except ValueError as e:
            return {"error": str(e)}, 401

        # Check if the user is an Admin
        if user["role"] != "Admin":
            return {"error": "Forbidden: Only Admins can delete destinations."}, 403

        # Find and remove the destination by ID
        global DESTINATIONS
        destination = next((dest for dest in DESTINATIONS if dest["id"] == id), None)
        if not destination:
            return {"error": "Destination not found"}, 404

        DESTINATIONS = [dest for dest in DESTINATIONS if dest["id"] != id]
        return {"message": f"Destination '{destination['name']}' deleted successfully."}, 200
