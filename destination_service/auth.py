# from functools import wraps
# from flask import request
# from jose import jwt
# from datetime import datetime
# import os

# # Secret key for JWT (you should keep this consistent between services or store it in an environment variable)
# SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

# # Mocked user data for illustration (replace with actual database or communication between services)
# USERS = [
#     {"id": "some-uuid", "name": "John Doe", "role": "Admin"},
#     {"id": "another-uuid", "name": "Jane Doe", "role": "User"}
# ]

# # Token validation decorator
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']
#             try:
#                 token = auth_header.split(" ")[1]
#             except IndexError:
#                 return {'message': 'Invalid token format. Use format: Bearer <token>'}, 401

#         if not token:
#             return {'message': 'Token is missing.'}, 401

#         try:
#             # Decode the token and get user data
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             current_user = next((user for user in USERS if user['id'] == data['user_id']), None)
#             if not current_user:
#                 return {'message': 'Invalid token. User not found.'}, 401
#             return f(current_user=current_user, *args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return {'message': 'Token has expired.'}, 401
#         except jwt.JWTError:
#             return {'message': 'Invalid token.'}, 401
#     return decorated

# # Admin-only access decorator
# def admin_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         current_user = kwargs.get('current_user', None)
#         if not current_user or current_user.get('role') != 'Admin':
#             return {'message': 'Unauthorized access. Admins only.'}, 403
#         return f(*args, **kwargs)
#     return decorated
