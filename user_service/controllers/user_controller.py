
from flask import Flask, request
from flask_restx import Api, Namespace, Resource, fields
import uuid
from datetime import datetime, timedelta
from jose import jwt
from utils.password_utils import hash_password, verify_password

# Mocked user data for simplicity (Replace with database in production)
USERS = [
    {
        "id": "some-uuid",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": hash_password("admin123"),  # Replace with pre-hashed password
        "role": "Admin"
    }
]

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# User Namespace
user_namespace = Namespace('user', description="User-related operations")
api.add_namespace(user_namespace, path='/user')

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

            print(f"Token Decoded Data: {data}")  # Debugging
            print(f"Current User: {current_user}")  # Debugging
            
            # Pass `current_user` as a keyword argument
            return f(current_user=dict(current_user), *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired.'}, 401
        except jwt.JWTError:
            return {'message': 'Invalid token.'}, 401
    return decorated



# User Registration Endpoint
@user_namespace.route("/register")
class Register(Resource):
    @user_namespace.expect(register_model)
    @user_namespace.response(201, "User registered successfully", profile_model)
    @user_namespace.response(400, "Email already registered")
    def post(self):
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


# User Login Endpoint
@user_namespace.route("/login")
class Login(Resource):
    @user_namespace.expect(login_model)
    @user_namespace.response(200, "Login successful")
    @user_namespace.response(400, "Invalid email or password")
    def post(self):
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


# User Profile Endpoint
@user_namespace.route("/profile")
class Profile(Resource):
    @user_namespace.doc(security='Bearer')
    @user_namespace.response(200, "Profile retrieved successfully", profile_model)
    @user_namespace.response(401, "Unauthorized")
    @user_namespace.response(404, "User not found")
    @user_namespace.param('user_id', 'User ID to fetch profile (optional)', _in='query')
    @token_required
    def get(self, current_user):
        print(f"Current User in Profile: {current_user}")  # Debugging
        print(f"Current User Type: {type(current_user)}")  # Debugging

        user_id = request.args.get("user_id")

        print(current_user)

        if user_id:
            if current_user['role'] != 'Admin' and current_user['id'] != user_id:
                return {"error": "Unauthorized to view this profile"}, 401

            user = next((user for user in USERS if user["id"] == user_id), None)
        else:
            user = current_user

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }, 200

