# app/utils/auth.py
from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                return jsonify({"message": "Token is missing"}), 401
            try:
                data = jwt.decode(token, os.getenv("SECRET_KEY", "mysecret"), algorithms=["HS256"])
                if role and data.get("role") != role:
                    return jsonify({"message": "Unauthorized role"}), 403
                request.user_id = data["user_id"]
                request.user_role = data["role"]
            except Exception:
                return jsonify({"message": "Invalid or expired token"}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator
