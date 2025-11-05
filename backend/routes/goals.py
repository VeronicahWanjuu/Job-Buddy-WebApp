"""
Goals routes for the JobBuddy API.

This module handles weekly goal management and gamification features
including streaks and points.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
from models import db
from models.goal import Goal
from models.streak import Streak
from models.notification import Notification
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for goals routes
goals_bp = Blueprint('goals', __name__, url_prefix='/api/v1/goals')


@goals_bp.route('/current', methods=['GET'])
@login_required
def get_current_goal():
    """
    Get current week's goal.
    
    Returns:
        JSON with current goal data
    """
    try:
        user_id = request.user_id
        
        # Get current week's Monday
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        
        goal = Goal.query.filter_by(user_id=user_id, week_start=week_start).first()
        
        if not goal:
            # Create goal if it doesn't exist
            goal = Goal(user_id=user_id, week_start=week_start)
            db.session.add(goal)
            db.session.commit()
        
        return jsonify({
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@goals_bp.route('', methods=['POST'])
@login_required
def set_goal():
    """
    Set weekly goals.
    
    Request body:
    {
        "applications_goal": 5,
        "outreach_goal": 3
    }
    
    Returns:
        JSON with updated goal data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data:
            raise APIError('Request body is required', 400)
        
        # Get current week's Monday
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        
        goal = Goal.query.filter_by(user_id=user_id, week_start=week_start).first()
        
        if not goal:
            goal = Goal(user_id=user_id, week_start=week_start)
            db.session.add(goal)
        
        # Update goals
        if 'applications_goal' in data:
            goal.applications_goal = max(0, int(data.get('applications_goal', 0)))
        
        if 'outreach_goal' in data:
            goal.outreach_goal = max(0, int(data.get('outreach_goal', 0)))
        
        db.session.commit()
        
        return jsonify({
            'message': 'Goals updated successfully',
            'goal': goal.to_dict()
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@goals_bp.route('/streak', methods=['GET'])
@login_required
def get_streak():
    """
    Get user's streak information.
    
    Returns:
        JSON with streak data
    """
    try:
        user_id = request.user_id
        
        streak = Streak.query.filter_by(user_id=user_id).first()
        
        if not streak:
            # Create streak if it doesn't exist
            streak = Streak(user_id=user_id)
            db.session.add(streak)
            db.session.commit()
        
        return jsonify({
            'streak': streak.to_dict()
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@goals_bp.route('/micro-quests', methods=['GET'])
@login_required
def get_micro_quests():
    """
    Get available micro-quests.
    
    Returns:
        JSON with list of micro-quests
    """
    try:
        # Load micro-quests from JSON file
        import json
        import os
        
        quests_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'micro_quests.json')
        
        if os.path.exists(quests_file):
            with open(quests_file, 'r') as f:
                quests = json.load(f)
        else:
            quests = [
                {
                    'id': 1,
                    'title': 'First Application',
                    'description': 'Submit your first job application',
                    'reward_points': 10
                },
                {
                    'id': 2,
                    'title': 'Networking Pro',
                    'description': 'Reach out to 3 contacts',
                    'reward_points': 25
                },
                {
                    'id': 3,
                    'title': 'CV Optimizer',
                    'description': 'Analyze your CV against a job description',
                    'reward_points': 15
                },
                {
                    'id': 4,
                    'title': 'Week Warrior',
                    'description': 'Complete your weekly goals',
                    'reward_points': 50
                }
            ]
        
        return jsonify({
            'quests': quests
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@goals_bp.route('/micro-quests/<int:quest_id>/complete', methods=['POST'])
@login_required
def complete_micro_quest(quest_id):
    """
    Mark a micro-quest as completed.
    
    Returns:
        JSON with updated streak and points
    """
    try:
        user_id = request.user_id
        
        streak = Streak.query.filter_by(user_id=user_id).first()
        
        if not streak:
            streak = Streak(user_id=user_id)
            db.session.add(streak)
        
        # Award points based on quest
        quest_points = {
            1: 10,
            2: 25,
            3: 15,
            4: 50
        }
        
        points = quest_points.get(quest_id, 10)
        streak.total_points += points
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            type='micro_quest',
            title='Quest Completed!',
            message=f'You earned {points} points for completing a quest!',
            related_type='goal'
        )
        db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quest completed!',
            'points_earned': points,
            'streak': streak.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
