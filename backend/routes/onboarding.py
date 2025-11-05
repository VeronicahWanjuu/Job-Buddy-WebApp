"""
Onboarding routes for the JobBuddy API.

This module handles the 7-step onboarding process for new users.
"""

import json
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db
from models.onboarding import OnboardingData
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for onboarding routes
onboarding_bp = Blueprint('onboarding', __name__, url_prefix='/api/v1/onboarding')


@onboarding_bp.route('', methods=['POST'])
@login_required
def create_onboarding():
    """
    Create or update onboarding data (7-step process).
    
    Request body:
    {
        "target_role": "Software Engineer",
        "target_industry": "Technology",
        "experience_level": "Mid",
        "dream_milestone": "Become a Tech Lead",
        "skills": ["Python", "React", "AWS"],
        "preferred_locations": ["San Francisco", "New York"],
        "availability": "Immediate"
    }
    
    Returns:
        JSON with onboarding data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data:
            raise APIError('Request body is required', 400)
        
        # Validate required fields
        required_fields = ['target_role', 'target_industry', 'experience_level', 
                          'dream_milestone', 'skills', 'preferred_locations', 'availability']
        
        for field in required_fields:
            if field not in data:
                raise APIError(f'Missing required field: {field}', 400)
        
        # Check if onboarding already exists
        onboarding = OnboardingData.query.filter_by(user_id=user_id).first()
        
        if onboarding and onboarding.completed_at:
            raise APIError('Onboarding has already been completed and cannot be modified', 403)
        
        if not onboarding:
            onboarding = OnboardingData(user_id=user_id)
        
        # Update onboarding data
        onboarding.target_role = data.get('target_role', '').strip()
        onboarding.target_industry = data.get('target_industry', '').strip()
        onboarding.experience_level = data.get('experience_level', '').strip()
        onboarding.dream_milestone = data.get('dream_milestone', '').strip()
        onboarding.availability = data.get('availability', '').strip()
        
        # Store skills and locations as JSON
        skills = data.get('skills', [])
        if isinstance(skills, list):
            onboarding.skills = json.dumps(skills)
        else:
            raise APIError('Skills must be an array', 400)
        
        preferred_locations = data.get('preferred_locations', [])
        if isinstance(preferred_locations, list):
            onboarding.preferred_locations = json.dumps(preferred_locations)
        else:
            raise APIError('Preferred locations must be an array', 400)
        
        # Mark as completed
        onboarding.completed_at = datetime.utcnow()
        
        db.session.add(onboarding)
        db.session.commit()
        
        return jsonify({
            'message': 'Onboarding completed successfully',
            'onboarding': onboarding.to_dict()
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@onboarding_bp.route('', methods=['GET'])
@login_required
def get_onboarding():
    """
    Get current user's onboarding data.
    
    Returns:
        JSON with onboarding data or 404 if not found
    """
    try:
        user_id = request.user_id
        
        onboarding = OnboardingData.query.filter_by(user_id=user_id).first()
        
        if not onboarding:
            raise APIError('Onboarding data not found', 404)
        
        return jsonify({
            'onboarding': onboarding.to_dict()
        }), 200
        
    except APIError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
