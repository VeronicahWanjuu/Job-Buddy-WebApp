"""
Notifications routes for the JobBuddy API.

This module handles in-app notification management.
"""

from flask import Blueprint, request, jsonify
from models import db
from models.notification import Notification
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for notifications routes
notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')


@notifications_bp.route('', methods=['GET'])
@login_required
def list_notifications():
    """
    Get all notifications for the current user.
    
    Query parameters:
    - is_read: Filter by read status (true/false)
    - type: Filter by notification type
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
        JSON with list of notifications and unread count
    """
    try:
        user_id = request.user_id
        
        # Get query parameters
        is_read = request.args.get('is_read')
        notification_type = request.args.get('type', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Notification.query.filter_by(user_id=user_id)
        
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            query = query.filter_by(is_read=is_read_bool)
        
        if notification_type:
            query = query.filter_by(type=notification_type)
        
        # Order by created_at descending
        query = query.order_by(Notification.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        notifications = [notif.to_dict() for notif in paginated.items]
        
        # Get unread count
        unread_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
        
        return jsonify({
            'notifications': notifications,
            'unread_count': unread_count,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@notifications_bp.route('/<int:id>/read', methods=['PUT'])
@login_required
def mark_as_read(id):
    """
    Mark a notification as read.
    
    Returns:
        JSON with updated notification
    """
    try:
        user_id = request.user_id
        
        notification = Notification.query.filter_by(id=id, user_id=user_id).first()
        if not notification:
            raise APIError('Notification not found', 404)
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@notifications_bp.route('/read-all', methods=['PUT'])
@login_required
def mark_all_as_read():
    """
    Mark all notifications as read for the current user.
    
    Returns:
        JSON success message
    """
    try:
        user_id = request.user_id
        
        # Update all unread notifications
        Notification.query.filter_by(user_id=user_id, is_read=False).update(
            {'is_read': True},
            synchronize_session=False
        )
        db.session.commit()
        
        return jsonify({
            'message': 'All notifications marked as read'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@notifications_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_notification(id):
    """
    Delete a notification.
    
    Returns:
        JSON success message
    """
    try:
        user_id = request.user_id
        
        notification = Notification.query.filter_by(id=id, user_id=user_id).first()
        if not notification:
            raise APIError('Notification not found', 404)
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Notification deleted successfully'
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
