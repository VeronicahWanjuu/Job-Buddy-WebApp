"""
User profile routes for the JobBuddy API.

This module handles user profile management, settings, and account deletion.
"""

from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from utils.validators import validate_password
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for profile routes
profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/profile')


@profile_bp.route('', methods=['GET'])
@login_required
def get_profile():
    """
    Get current user's profile.
    
    Returns:
        JSON with user profile data and statistics
    """
    try:
        user = request.current_user
        
        return jsonify({
            'user': user.to_dict(include_stats=True)
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@profile_bp.route('', methods=['PUT'])
@login_required
def update_profile():
    """
    Update user profile information.
    
    Request body:
    {
        "name": "New Name",
        "dream_milestone": "Become a Senior Software Engineer"
    }
    
    Returns:
        JSON with updated user data
    """
    try:
        user = request.current_user
        data = request.get_json()
        
        if not data:
            raise APIError('Request body is required', 400)
        
        # Update name if provided
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name or len(name) < 2:
                raise APIError('Name must be at least 2 characters long', 400)
            user.name = name
        
        # Update dream milestone if provided
        if 'dream_milestone' in data:
            user.dream_milestone = data.get('dream_milestone', '').strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@profile_bp.route('/password', methods=['PUT'])
@login_required
def change_password():
    """
    Change user password.
    
    Request body:
    {
        "current_password": "OldPass123",
        "new_password": "NewPass123"
    }
    
    Returns:
        JSON success message
    """
    try:
        user = request.current_user
        data = request.get_json()
        
        if not data or not all(k in data for k in ['current_password', 'new_password']):
            raise APIError('Missing required fields: current_password, new_password', 400)
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Verify current password
        if not user.check_password(current_password):
            raise APIError('Current password is incorrect', 401, 'INVALID_PASSWORD')
        
        # Validate new password
        validate_password(new_password)
        
        # Check that new password is different from current
        if current_password == new_password:
            raise APIError('New password must be different from current password', 400)
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@profile_bp.route('', methods=['DELETE'])
@login_required
def delete_account():
    """
    Delete user account and all associated data.
    
    Returns:
        JSON success message
    """
    try:
        user = request.current_user
        
        # Delete user (cascade will delete all related data)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Account deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
