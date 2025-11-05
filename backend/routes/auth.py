"""
Authentication routes for the JobBuddy API.

This module handles user registration, login, logout, and password recovery.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from models import db
from models.user import User
from models.streak import Streak
from models.goal import Goal
from utils.validators import validate_email, validate_password, validate_job_title
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123",
        "name": "John Doe"
    }
    
    Returns:
        JSON with user data and access token
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password', 'name']):
            raise APIError('Missing required fields: email, password, name', 400)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validate inputs
        validate_email(email)
        validate_password(password)
        
        if not name or len(name) < 2:
            raise APIError('Name must be at least 2 characters long', 400)
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise APIError('Email already registered', 400, 'EMAIL_EXISTS')
        
        # Create new user
        user = User(email=email, name=name)
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create initial streak record
        streak = Streak(user_id=user.id)
        db.session.add(streak)
        
        # Create initial goal record (for current week)
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())  # Monday of current week
        
        goal = Goal(user_id=user.id, week_start=week_start)
        db.session.add(goal)
        
        db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123"
    }
    
    Returns:
        JSON with user data and access token
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password']):
            raise APIError('Missing required fields: email, password', 400)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise APIError('Invalid email or password', 401, 'INVALID_CREDENTIALS')
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except APIError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logout user (token-based, so just return success).
    
    Returns:
        JSON success message
    """
    return jsonify({
        'message': 'Logout successful'
    }), 200


@auth_bp.route('/password-recovery', methods=['POST'])
def password_recovery():
    """
    Initiate password recovery (placeholder for email integration).
    
    Request body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        JSON success message
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            raise APIError('Email is required', 400)
        
        email = data.get('email', '').strip()
        validate_email(email)
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            # For security, don't reveal if email exists
            return jsonify({
                'message': 'If an account exists with this email, a recovery link has been sent'
            }), 200
        
        # TODO: Send password recovery email
        # For now, just return success
        
        return jsonify({
            'message': 'If an account exists with this email, a recovery link has been sent'
        }), 200
        
    except APIError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
