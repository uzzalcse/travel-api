# from flask import request, jsonify
# import jwt

# SECRET_KEY = "your-secret-key"

# def admin_required(func):
#     def wrapper(*args, **kwargs):
#         token = request.headers.get("Authorization")
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             if payload.get("role") != "Admin":
#                 return jsonify({"error": "Forbidden"}), 403
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"error": "Invalid token"}), 401

#         return func(*args, **kwargs)
#     return wrapper
