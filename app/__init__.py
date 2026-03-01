from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import config
from app.models import db
from app.routes import register_blueprints
from app.error_handlers import register_error_handlers

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         headers=["Content-Type", "Authorization"])
    
    # Register error handlers and blueprints
    register_error_handlers(app)
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
