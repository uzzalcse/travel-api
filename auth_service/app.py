import warnings

# Ignore deprecation warnings in the app
warnings.filterwarnings("ignore", category=DeprecationWarning)


from flask import Flask
from flask_restx import Api
from controllers.auth_controller import auth_namespace  # Import the auth controller namespace
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_restx")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="jose.jwt")

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
    title="Authentication Service API",
    description="API for validating tokens and checking user roles",
    authorizations=authorizations,  # Add authorizations here
    security='Bearer'  # Apply Bearer token globally
)

# Register the auth namespace
api.add_namespace(auth_namespace, path="/auth")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
