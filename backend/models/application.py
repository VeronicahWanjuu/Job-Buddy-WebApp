from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    """
    Application model for tracking job applications.
    
    This model represents a job application that the user has submitted or plans to submit.
    It tracks the status of the application through the Kanban board columns:
    Planned -> Applied -> Interview -> Offer -> Rejected
    """
    __tablename__ = 'applications'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)

    # Application information
    job_title = db.Column(db.String(255), nullable=False)  # Job title (min 3 chars)
    job_url = db.Column(db.String(255))  # Link to job posting
    status = db.Column(db.String(50), nullable=False, default='Planned', index=True)
    # Status options: Planned, Applied, Interview, Offer, Rejected
    applied_date = db.Column(db.Date)  # Date when application was submitted
    notes = db.Column(db.Text)  # User's notes about the application

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    outreach_activities = db.relationship('OutreachActivity', backref='application', lazy='dynamic')
    cv_analyses = db.relationship('CVAnalysis', backref='application', lazy='dynamic')

    def to_dict(self, include_company=False):
        """
        Convert application to dictionary for API responses.
        
        Args:
            include_company (bool): Whether to include company details
            
        Returns:
            dict: Application data as dictionary
        """
        app_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'job_title': self.job_title,
            'job_url': self.job_url,
            'status': self.status,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_company and self.company:
            app_dict['company'] = self.company.to_dict()

        return app_dict

    def __repr__(self):
        return f'<Application {self.job_title} at {self.company.name if self.company else "Unknown"}>'
