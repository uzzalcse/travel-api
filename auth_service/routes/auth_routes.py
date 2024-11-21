from flask import Blueprint
from auth_service.controllers.auth_controller import login, validate_token
from auth_service.utils.decorators import role_required

auth_bp = Blueprint('auth', __name__)

# Route for user login
auth_bp.route('/login', methods=['POST'])(login)

# Example of a protected route requiring Admin role
@auth_bp.route('/admin-only', methods=['GET'])
@role_required('Admin')
def admin_only():
    return "This is a protected Admin route", 200
