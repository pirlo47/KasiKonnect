from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["JWT_SECRET_KEY"] = "supersecretkey"
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    from .routes import auth
    app.register_blueprint(auth.bp)
    
    @app.route('/')
    def index():
        return render_template('login.html')
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app
