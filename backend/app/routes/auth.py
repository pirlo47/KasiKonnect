from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from msal import PublicClientApplication  # Microsoft Authentication

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "supersecretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50))  # service_provider or client
    location = db.Column(db.String(200), nullable=True)
    display_picture = db.Column(db.String(200))

# Microsoft Authentication setup
client_id = "4eb43f02-6f25-41cb-8c9f-2248d5b16f25"
tenant_id = "3d972777-ed64-4708-b162-3314801c7198"
authority = f"https://login.microsoftonline.com/{tenant_id}"
msal_client = PublicClientApplication(client_id, authority=authority)

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.json
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

@app.route("/auth/microsoft-login", methods=["GET"])
def microsoft_login():
    auth_url = msal_client.get_authorization_request_url(["user.read"])
    return jsonify({"auth_url": auth_url})

if __name__ == "__main__":
    app.run(debug=True)
