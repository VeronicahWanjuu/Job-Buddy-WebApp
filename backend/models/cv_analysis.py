from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CVAnalysis(db.Model):
    """
    CV analysis model for storing CV-JD keyword matching results.
    
    This model stores the results of CV and job description analysis,
    including ATS scores, matched keywords, missing keywords, and suggestions.
    """
    __tablename__ = 'cv_analyses'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=True, index=True)

    # File and content information
    cv_filename = db.Column(db.String(255))  # Name of uploaded CV file
    job_description = db.Column(db.Text, nullable=False)  # Job description text

    # Analysis results
    ats_score = db.Column(db.Integer)  # ATS score (0-100)
    matched_keywords = db.Column(db.Text)  # JSON array of matched keywords
    missing_keywords = db.Column(db.Text)  # JSON array of missing keywords
    suggestions = db.Column(db.Text)  # JSON array of improvement suggestions

    # Metadata
    api_used = db.Column(db.String(50))  # Which API was used for analysis (or 'custom')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """
        Convert CV analysis to dictionary for API responses.
        
        Returns:
            dict: CV analysis data as dictionary with parsed JSON arrays
        """
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'application_id': self.application_id,
            'cv_filename': self.cv_filename,
            'job_description': self.job_description,
            'ats_score': self.ats_score,
            'matched_keywords': json.loads(self.matched_keywords) if self.matched_keywords else [],
            'missing_keywords': json.loads(self.missing_keywords) if self.missing_keywords else [],
            'suggestions': json.loads(self.suggestions) if self.suggestions else [],
            'api_used': self.api_used,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<CVAnalysis user_id={self.user_id} score={self.ats_score}>'
