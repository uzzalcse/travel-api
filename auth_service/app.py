from flask import Flask
from auth_service.routes.auth_routes import auth_bp
from flask_cors import CORS  # Optional: enables cross-origin requests

# Initialize the Flask app
app = Flask(__name__)

# Enable cross-origin requests if needed
CORS(app)

# Secret key for JWT encoding/decoding
app.config['SECRET_KEY'] = 'supersecretkey'

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run auth_service on port 5001
