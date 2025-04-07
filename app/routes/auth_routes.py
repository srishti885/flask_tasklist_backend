
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = generate_password_hash(data["password"], method='sha256')
    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_pw,
        role=data.get("role", "user")
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, os.getenv("SECRET_KEY", "mysecret"), algorithm="HS256")

    return jsonify({"token": token}), 200
