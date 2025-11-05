from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goal(db.Model):
    """
    Goal model for tracking weekly job search goals.
    
    This model stores the user's weekly goals for applications and outreach activities.
    Goals reset every Monday at midnight UTC. The user can only edit goals once per week.
    """
    __tablename__ = 'goals'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Goal tracking
    week_start = db.Column(db.Date, nullable=False, index=True)  # Monday of the week
    applications_goal = db.Column(db.Integer, default=0)  # Target number of applications
    applications_current = db.Column(db.Integer, default=0)  # Current count of applications
    outreach_goal = db.Column(db.Integer, default=0)  # Target number of outreach activities
    outreach_current = db.Column(db.Integer, default=0)  # Current count of outreach activities

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Unique constraint: one goal per user per week
    __table_args__ = (
        db.UniqueConstraint('user_id', 'week_start', name='unique_user_week_goal'),
    )

    def to_dict(self):
        """
        Convert goal to dictionary for API responses.
        
        Returns:
            dict: Goal data as dictionary with progress percentages
        """
        # Calculate progress percentages
        applications_progress = 0
        outreach_progress = 0

        if self.applications_goal > 0:
            applications_progress = min(100, int((self.applications_current / self.applications_goal) * 100))
        if self.outreach_goal > 0:
            outreach_progress = min(100, int((self.outreach_current / self.outreach_goal) * 100))

        return {
            'id': self.id,
            'user_id': self.user_id,
            'week_start': self.week_start.isoformat() if self.week_start else None,
            'applications_goal': self.applications_goal,
            'applications_current': self.applications_current,
            'applications_progress': applications_progress,
            'outreach_goal': self.outreach_goal,
            'outreach_current': self.outreach_current,
            'outreach_progress': outreach_progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Goal user_id={self.user_id} week={self.week_start}>'
