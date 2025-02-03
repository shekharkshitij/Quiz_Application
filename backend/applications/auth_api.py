from flask_restful import Resource
from flask import request, jsonify
from applications.model import User
from applications.database import db
from applications.user_datastore import user_datastore
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re
import logging

logging.basicConfig(level=logging.INFO)

# JWT Configuration
SECRET_KEY = "your_secret_key"  # Replace with a secure secret key
TOKEN_EXPIRY_HOURS = 24

# Utility functions
def is_valid_email(email):
    """Validate email format."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email))

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must include at least one number."
    if not any(char.isalpha() for char in password):
        return False, "Password must include at least one letter."
    if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
        return False, "Password must include both uppercase and lowercase letters."
    return True, ""

def generate_jwt(user):
    """Generate JWT token."""
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.roles[0].name if user.roles else "user",
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    """Decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}

# Resource for user login
class Login(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not email or not password:
            return {"message": "Email and password are required"}, 400

        # Find user and verify credentials
        user = user_datastore.find_user(email=email)
        if user:
            logging.info(f"User found: {email}")
            if check_password_hash(user.password, password):
                logging.info(f"Password verified for user: {email}")
                token = generate_jwt(user)
                return {"message": "Logged in successfully", "auth_token": token}, 200

        logging.warning(f"Failed login attempt for email: {email}")
        return {"message": "Invalid email or password"}, 401

# Resource for user registration
class Register(Resource):
    def post(self):
        data = request.json

        # Input validation
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        if not all([email, password, username]):
            return {"message": "Email, password, and username are required."}, 400

        if not is_valid_email(email):
            return {"message": "Invalid email format."}, 400

        password_valid, password_message = validate_password(password)
        if not password_valid:
            return {"message": password_message}, 400

        dob_str = data.get('dob')
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        except ValueError:
            return {"message": "Invalid date format for dob. Use 'YYYY-MM-DD'."}, 400

        # Check if the user already exists
        if user_datastore.find_user(email=email):
            logging.warning(f"Registration attempt with existing email: {email}")
            return {"message": "Email already exists"}, 400

        # Create user with hashed password
        try:
            user = user_datastore.create_user(
                username=username,
                email=email,
                password=generate_password_hash(password),
                full_name=data.get('full_name', ''),
                qualification=data.get('qualification', ''),
                dob=dob,
                roles=[user_datastore.find_or_create_role(name="user")]
            )
            db.session.commit()
            logging.info(f"User registered successfully: {email}")
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return {"message": "An error occurred during registration. Please try again later."}, 500

# Resource for user logout
class Logout(Resource):
    def post(self):
        # Logout in JWT-based systems is a client-side operation
        token = request.headers.get("Authorization")
        if token:
            try:
                token_data = decode_jwt(token)
                if "error" in token_data:
                    return {"message": token_data["error"]}, 401
                logging.info(f"User logged out: {token_data.get('email')}")
                return {"message": "Logged out successfully"}, 200
            except Exception as e:
                logging.error(f"Error during logout: {e}")
                return {"message": "An error occurred during logout."}, 500
        return {"message": "No token provided for logout."}, 400

# Middleware for role-based access control
def role_required(required_role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return {"message": "Authorization token is required"}, 401

            token_data = decode_jwt(token)
            if "error" in token_data:
                return {"message": token_data["error"]}, 401

            if token_data.get("role") != required_role:
                return {"message": "Access denied: insufficient privileges"}, 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
