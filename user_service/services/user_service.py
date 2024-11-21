# import uuid
# from utils.password_utils import hash_password, verify_password
# from models.user import USERS

# def register_user(data):
#     """
#     Registers a new user and stores their details in memory.
#     """
#     email = data.get("email")
#     if any(user["email"] == email for user in USERS):
#         raise ValueError("Email already registered")

#     user_id = str(uuid.uuid4())
#     hashed_password = hash_password(data["password"])

#     new_user = {
#         "id": user_id,
#         "name": data["name"],
#         "email": email,
#         "password": hashed_password,
#         "role": data.get("role", "User"),  # Default role is "User"
#     }
#     USERS.append(new_user)
#     print(USERS)
#     return {"id": user_id, "name": data["name"], "email": email, "role": new_user["role"]}

# def login_user(data):
#     """
#     Authenticates a user and returns a token.
#     """
#     from auth_service.utils.decorators import SECRET_KEY  # Reuse secret key for token generation
#     import jwt

#     email = data.get("email")
#     password = data.get("password")

#     # Find the user by email
#     user = next((user for user in USERS if user["email"] == email), None)
#     if not user or not verify_password(password, user["password"]):
#         raise ValueError("Invalid email or password")

#     # Generate JWT token
#     token = jwt.encode({"user_id": user["id"], "role": user["role"]}, SECRET_KEY, algorithm="HS256")
#     return token

# def get_user_profile(user_id):
#     """
#     Retrieves the profile of a user by their ID.
#     """
#     print(user_id)
#     user = next((user for user in USERS if user["id"] == user_id), None)
#     if not user:
#         raise ValueError("User not found")

#     return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}


from flask_restx import Namespace, Resource, fields
from flask import request
import uuid
import jwt
from datetime import datetime, timedelta
from models.user import USERS
from utils.password_utils import hash_password, verify_password

# Secret key for JWT
SECRET_KEY = "your_secret_key"

user_namespace = Namespace("user", description="User-related operations")

# Define Swagger Models
register_model = user_namespace.model(
    "Register",
    {
        "name": fields.String(required=True, description="User's full name"),
        "email": fields.String(required=True, description="User's email address"),
        "password": fields.String(required=True, description="User's password"),
        "role": fields.String(description="User's role (optional, defaults to 'User')"),
    },
)

login_model = user_namespace.model(
    "Login",
    {
        "email": fields.String(required=True, description="User's email address"),
        "password": fields.String(required=True, description="User's password"),
    },
)

profile_model = user_namespace.model(
    "Profile",
    {
        "id": fields.String(description="User ID"),
        "name": fields.String(description="User's full name"),
        "email": fields.String(description="User's email address"),
        "role": fields.String(description="User's role"),
    },
)

@user_namespace.route("/register")
class Register(Resource):
    @user_namespace.expect(register_model)
    @user_namespace.response(201, "User registered successfully", profile_model)
    @user_namespace.response(400, "Email already registered")
    def post(self):
        """
        Register a new user
        """
        data = user_namespace.payload
        email = data.get("email")
        if any(user["email"] == email for user in USERS):
            return {"error": "Email already registered"}, 400

        user_id = str(uuid.uuid4())
        hashed_password = hash_password(data["password"])

        new_user = {
            "id": user_id,
            "name": data["name"],
            "email": email,
            "password": hashed_password,
            "role": data.get("role", "User"),
        }
        USERS.append(new_user)
        return {"id": user_id, "name": data["name"], "email": email, "role": new_user["role"]}, 201


@user_namespace.route("/login")
class Login(Resource):
    @user_namespace.expect(login_model)
    @user_namespace.response(200, "Login successful", fields.String(description="JWT Token"))
    @user_namespace.response(400, "Invalid email or password")
    def post(self):
        """
        Authenticate a user and return a JWT token
        """
        data = user_namespace.payload
        email = data.get("email")
        password = data.get("password")

        user = next((user for user in USERS if user["email"] == email), None)
        if not user or not verify_password(password, user["password"]):
            return {"error": "Invalid email or password"}, 400

        token = jwt.encode(
            {"user_id": user["id"], "role": user["role"], "exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256",
        )
        return {"token": token}, 200


@user_namespace.route("/profile")
class Profile(Resource):
    @user_namespace.response(200, "Profile retrieved successfully", profile_model)
    @user_namespace.response(404, "User not found")
    def get(self):
        """
        Get the profile of a user by their ID
        """
        user_id = user_namespace.parser().parse_args().get("User-Id")
        user = next((user for user in USERS if user["id"] == user_id), None)
        if not user:
            return {"error": "User not found"}, 404

        return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}, 200
