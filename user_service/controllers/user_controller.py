from flask_restx import Namespace, Resource, fields
import uuid
from datetime import datetime, timedelta
from jose import jwt
from utils.password_utils import hash_password, verify_password

# Mock user data for this example (you can replace this with a database)
USERS = []

# Define user namespace
user_namespace = Namespace('user', description="User-related operations")

# Swagger Models
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

# Secret key for JWT (make sure to replace with a real secret key)
SECRET_KEY = "your_secret_key"

# JWT Token required decorator
def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {'message': 'Invalid token format. Use format: Bearer <token>'}, 401
        
        if not token:
            return {'message': 'Token is missing.'}, 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = next((user for user in USERS if user['id'] == data['user_id']), None)
            if current_user is None:
                return {'message': 'Invalid token. User not found.'}, 401
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired.'}, 401
        except jwt.JWTError:
            return {'message': 'Invalid token.'}, 401
        return f(current_user, *args, **kwargs)
    return decorated

# Register user
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

# Login user
@user_namespace.route("/login")
class Login(Resource):
    @user_namespace.expect(login_model)
    @user_namespace.response(200, "Login successful")
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
            {
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"token": token}, 200

# Get user profile
# @user_namespace.route("/profile")
# class Profile(Resource):
#     @user_namespace.doc(security='Bearer')  # This links to the API security definition
#     @user_namespace.response(200, "Profile retrieved successfully", profile_model)
#     @user_namespace.response(401, "Unauthorized")
#     @user_namespace.response(404, "User not found")
#     @user_namespace.param('user_id', 'User ID to fetch profile (optional)', _in='query')
#     @token_required
#     def get(self, current_user):
#         """
#         Get the profile of a user by their ID or token
#         """
#         user_id = request.args.get("user_id")
        
#         if user_id:
#             # If user_id is provided, check if the current user has permission to view it
#             if current_user['role'] != 'Admin' and current_user['id'] != user_id:
#                 return {"error": "Unauthorized to view this profile"}, 401
            
#             user = next((user for user in USERS if user["id"] == user_id), None)
#         else:
#             # If no user_id is provided, return the current user's profile
#             user = current_user

#         if not user:
#             return {"error": "User not found"}, 404

#         return {
#             "id": user["id"],
#             "name": user["name"],
#             "email": user["email"],
#             "role": user["role"]
#         }, 200


@user_namespace.route("/profile")
class Profile(Resource):
    @user_namespace.doc(security='Bearer')  # This links to the API security definition
    @user_namespace.response(200, "Profile retrieved successfully", profile_model)
    @user_namespace.response(401, "Unauthorized")
    @user_namespace.response(404, "User not found")
    @user_namespace.param('user_id', 'User ID to fetch profile (optional)', _in='query')
    @token_required
    def get(self, current_user):
        """
        Get the profile of a user by their ID or token
        """
        try:
            user_id = request.args.get("user_id")  # Fetch 'user_id' from query params
            
            if user_id:
                # If user_id is provided, check if the current user has permission to view it
                if current_user['role'] != 'Admin' and current_user['id'] != user_id:
                    return {"error": "Unauthorized to view this profile"}, 401
                
                # Fetch the user based on the user_id
                user = next((user for user in USERS if user["id"] == user_id), None)
            else:
                # If no user_id is provided, return the current user's profile
                user = current_user

            if not user:
                return {"error": "User not found"}, 404

            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }, 200
        except Exception as e:
            # Log the exception for debugging purposes
            return {"error": f"An error occurred: {str(e)}"}, 500
