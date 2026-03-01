from flask import Blueprint, jsonify
from app.models import db

health_bp = Blueprint("health", __name__, url_prefix="/api")

@health_bp.route("/health", methods=["GET"])
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return jsonify({
        "status": "healthy",
        "message": "Flask API is running",
        "database": db_status
    }), 200
