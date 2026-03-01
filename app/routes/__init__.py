from flask import Flask
from app.routes.health import health_bp

def register_blueprints(app: Flask):
    app.register_blueprint(health_bp)
from app.routes.auth_routes import auth_bp
__all__ = ['auth_bp']
