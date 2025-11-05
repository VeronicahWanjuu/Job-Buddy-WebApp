from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notification(db.Model):
    """
    Notification model for in-app notifications.
    
    This model stores in-app notifications for the user. Notifications are created
    automatically based on user actions and can be marked as read or deleted.
    
    Types of notifications:
    - follow_up: Reminder to follow up on an application
    - goal_reminder: Reminder about weekly goal progress
    - micro_quest: Notification about completed micro-quests
    - system: General system alerts
    """
    __tablename__ = 'notifications'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Notification information
    type = db.Column(db.String(50), nullable=False, index=True)  # follow_up, goal_reminder, micro_quest, system
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text)

    # Link to related item
    related_type = db.Column(db.String(50))  # application, outreach, goal, etc.
    related_id = db.Column(db.Integer)  # ID of related item

    # Status
    is_read = db.Column(db.Boolean, default=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        """
        Convert notification to dictionary for API responses.
        
        Returns:
            dict: Notification data as dictionary
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'related_type': self.related_type,
            'related_id': self.related_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Notification user_id={self.user_id} type={self.type}>'
