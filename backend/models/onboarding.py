from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OnboardingData(db.Model):
    """
    Onboarding data model for storing user's initial setup information.
    
    This model stores the 7-step onboarding data that users provide when first
    creating their account. Each user can only have one onboarding record.
    """
    __tablename__ = 'onboarding_data'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)

    # Onboarding fields (from the 7-step process)
    target_role = db.Column(db.String(255), nullable=False)  # Step 1: Target job role
    target_industry = db.Column(db.String(255))  # Step 2: Target industry
    experience_level = db.Column(db.String(50))  # Step 3: Experience level (Junior, Mid, Senior)
    dream_milestone = db.Column(db.Text)  # Step 4: Dream milestone/goal
    skills = db.Column(db.Text)  # Step 5: Skills (JSON array stored as text)
    preferred_locations = db.Column(db.Text)  # Step 6: Preferred locations (JSON array stored as text)
    availability = db.Column(db.String(50))  # Step 7: Availability (Immediate, 1-3 months, etc.)

    # Completion tracking
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """
        Convert onboarding data to dictionary for API responses.
        
        Returns:
            dict: Onboarding data as dictionary with parsed JSON arrays
        """
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_role': self.target_role,
            'target_industry': self.target_industry,
            'experience_level': self.experience_level,
            'dream_milestone': self.dream_milestone,
            'skills': json.loads(self.skills) if self.skills else [],
            'preferred_locations': json.loads(self.preferred_locations) if self.preferred_locations else [],
            'availability': self.availability,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<OnboardingData user_id={self.user_id}>'
