# from flask import Blueprint
# from controllers.user_controller import register, login, profile

# user_blueprint = Blueprint("user", __name__)
# user_blueprint.add_url_rule("/register", "register", register, methods=["POST"])
# user_blueprint.add_url_rule("/login", "login", login, methods=["POST"])
# user_blueprint.add_url_rule("/profile", "profile", profile, methods=["GET"])


from flask_restx import Namespace, Resource, fields
from services.user_service import register_user, login_user, get_user_profile

# Create a Namespace for Swagger
user_namespace = Namespace("user", description="User management endpoints")

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


# Register Route
@user_namespace.route("/register")
class Register(Resource):
    @user_namespace.expect(register_model)
    @user_namespace.response(201, "User registered successfully", profile_model)
    @user_namespace.response(400, "Email already registered")
    def post(self):
        """
        Register a new user
        """
        try:
            data = user_namespace.payload
            return register_user(data), 201
        except ValueError as e:
            return {"error": str(e)}, 400


# Login Route
@user_namespace.route("/login")
class Login(Resource):
    @user_namespace.expect(login_model)
    @user_namespace.response(200, "Login successful", fields.String(description="JWT Token"))
    @user_namespace.response(400, "Invalid email or password")
    def post(self):
        """
        Authenticate a user and return a JWT token
        """
        try:
            data = user_namespace.payload
            return {"token": login_user(data)}, 200
        except ValueError as e:
            return {"error": str(e)}, 400


# Profile Route
@user_namespace.route("/profile")
class Profile(Resource):
    @user_namespace.response(200, "Profile retrieved successfully", profile_model)
    @user_namespace.response(404, "User not found")
    def get(self):
        """
        Retrieve a user's profile by their ID
        """
        try:
            # Assuming User ID is passed in the headers
            user_id = user_namespace.parser().parse_args().get("User-Id")
            return get_user_profile(user_id), 200
        except ValueError as e:
            return {"error": str(e)}, 404
