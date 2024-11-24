

import warnings
from flask import request
from flask_restx import Namespace, Resource, fields
from jose import jwt

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_restx.api")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="jsonschema")

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# Define the Namespace
auth_namespace = Namespace("auth", description="Authentication and Role Validation")

# Swagger Models
token_validation_model = auth_namespace.model(
    "TokenValidation",
    {
        "token": fields.String(required=True, description="JWT token to validate")
    },
)

role_response_model = auth_namespace.model(
    "RoleResponse",
    {
        "user_id": fields.String(description="User ID"),
        "role": fields.String(description="User role (Admin/User)"),
    },
)

# Token Validation Endpoint
@auth_namespace.route("/validate")
class TokenValidation(Resource):
    @auth_namespace.expect(token_validation_model)
    @auth_namespace.response(200, "Token validated successfully", role_response_model)
    @auth_namespace.response(401, "Invalid or expired token")
    def post(self):
        """
        Validate the provided JWT token and return the user's role.
        """
        data = auth_namespace.payload
        token = data.get("token")
        
        if not token:
            return {"error": "Token is missing."}, 401
        
        try:
            # Decode the JWT token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get("user_id")
            role = decoded.get("role")
            
            if not user_id or not role:
                return {"error": "Invalid token payload."}, 401
            
            return {"user_id": user_id, "role": role}, 200
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}, 401
        except jwt.JWTError:
            return {"error": "Invalid token."}, 401
