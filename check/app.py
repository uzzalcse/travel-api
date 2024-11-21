from flask import Flask
from flask_restx import Api, Namespace, Resource

app = Flask(__name__)

# Define authorizations for JWT Bearer token
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "JWT token in the Authorization header. Use format: Bearer <JWT>"
    }
}

# Initialize Flask-RESTX API with authorizations
api = Api(app, 
          version='1.0', 
          title='API with Authorization', 
          description='A simple API with Authorization feature',
          authorizations=authorizations,
          security='Bearer')  # Security requirement for all endpoints

# Define a simple namespace
namespace = Namespace('example', description='Example API')

# Define a simple resource
@namespace.route('/hello')
class HelloWorld(Resource):
    @namespace.doc(security='Bearer')  # Apply security for authorization
    def get(self):
        return {'message': 'Hello, World!'}

# Add the namespace to the API
api.add_namespace(namespace)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
