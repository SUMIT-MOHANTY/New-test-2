import bcrypt
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    
    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email, password_hash=AuthService.hash_password(password))
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def authenticate_user(email, password):
        user = AuthService.get_user_by_email(email)
        if user and AuthService.check_password(password, user.password_hash):
            return user
        return None
    
    @staticmethod
    def generate_tokens(user):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return access_token, refresh_token
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
