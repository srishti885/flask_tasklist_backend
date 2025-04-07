from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token != "Bearer mysecrettoken":
            return jsonify({"message": "Token is missing or invalid"}), 401
        return f(*args, **kwargs)
    return decorated
