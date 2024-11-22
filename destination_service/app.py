from flask import Flask
from flask_restx import Api
from controllers.destination_controller import destination_namespace  # Import the destination controller namespace

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
    title="Destination Service API",
    description="API for managing destinations (adding, viewing)",
    authorizations=authorizations,  # Add authorizations here
    security='Bearer'  # Apply Bearer token globally
)

# Register the destination namespace
api.add_namespace(destination_namespace, path="/destination")

if __name__ == "__main__":
    app.run(debug=True, port=5005)
