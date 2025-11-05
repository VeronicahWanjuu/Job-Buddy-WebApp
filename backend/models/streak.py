from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Streak(db.Model):
    """
    Streak model for tracking user activity streaks and points.
    
    This model tracks the user's current streak, longest streak, and total points.
    The streak increments on daily activity and resets if no activity for 24 hours.
    Activities that count: add application, log outreach, complete micro-quest.
    """
    __tablename__ = 'streaks'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)

    # Streak tracking
    current_streak = db.Column(db.Integer, default=0)  # Current streak count (days)
    longest_streak = db.Column(db.Integer, default=0)  # Longest streak achieved (days)
    last_activity_date = db.Column(db.Date)  # Last date of activity
    total_points = db.Column(db.Integer, default=0)  # Gamification points

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """
        Convert streak to dictionary for API responses.
        
        Returns:
            dict: Streak data as dictionary
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity_date': self.last_activity_date.isoformat() if self.last_activity_date else None,
            'total_points': self.total_points,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Streak user_id={self.user_id} current={self.current_streak} longest={self.longest_streak}>'
