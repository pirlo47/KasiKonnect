from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from msal import PublicClientApplication
from app.models import db, User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

# Microsoft Authentication Setup
client_id = "4eb43f02-6f25-41cb-8c9f-2248d5b16f25"
tenant_id = "3d972777-ed64-4708-b162-3314801c7198"
authority = f"https://login.microsoftonline.com/{tenant_id}"
msal_client = PublicClientApplication(client_id, authority=authority)

# Signup Route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_pw,
        role=data["role"],
        location=data.get("location"),
        display_picture=data.get("display_picture")
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# Microsoft Login Integration
@auth_bp.route("/microsoft-login", methods=["GET"])
def microsoft_login():
    auth_url = msal_client.get_authorization_request_url(["user.read"])
    return jsonify({"auth_url": auth_url})
