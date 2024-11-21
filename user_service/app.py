from flask import Flask
from flask_restx import Api
from controllers.user_controller import user_namespace  # Import the user controller namespace

# Define authorizations for JWT Bearer token
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "JWT token in the Authorization header. Use format: Bearer <JWT>"
    }
}

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTX API with the security settings
api = Api(
    app,
    version="1.0",
    title="User Management API",
    description="API for managing users (registration, login, profile)",
    authorizations=authorizations,  # Add authorizations here
    security='Bearer'  # Apply Bearer token globally
)

# Register the user namespace
api.add_namespace(user_namespace, path="/user")

if __name__ == "__main__":
    app.run(debug=True)
