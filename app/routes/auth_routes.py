from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_username, validate_password

auth_bp = Blueprint('auth', __name__)

# In-memory token blocklist for logout
token_blocklist = set()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided', 'code': 'NO_DATA'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields', 'code': 'MISSING_FIELDS'}), 400
    
    valid, error = validate_username(username)
    if not valid:
        return jsonify({'error': error, 'code': 'INVALID_USERNAME'}), 400
    
    valid, error = validate_email(email)
    if not valid:
        return jsonify({'error': error, 'code': 'INVALID_EMAIL'}), 400
    
    valid, error = validate_password(password)
    if not valid:
        return jsonify({'error': error, 'code': 'INVALID_PASSWORD'}), 400
    
    if AuthService.get_user_by_username(username):
        return jsonify({'error': 'Username already exists', 'code': 'USERNAME_EXISTS'}), 409
    
    if AuthService.get_user_by_email(email):
        return jsonify({'error': 'Email already exists', 'code': 'EMAIL_EXISTS'}), 409
    
    user = AuthService.create_user(username, email, password)
    access_token, refresh_token = AuthService.generate_tokens(user)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided', 'code': 'NO_DATA'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Missing email or password', 'code': 'MISSING_FIELDS'}), 400
    
    user = AuthService.authenticate_user(email, password)
    
    if not user:
        return jsonify({'error': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is inactive', 'code': 'ACCOUNT_INACTIVE'}), 401
    
    access_token, refresh_token = AuthService.generate_tokens(user)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token_blocklist.add(jti)
    return jsonify({'message': 'Successfully logged out'}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200

# JWT token blocklist callback
@auth_bp.before_app_request
def check_token_not_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    if jti in token_blocklist:
        return jsonify({'error': 'Token has been revoked', 'code': 'TOKEN_REVOKED'}), 401
