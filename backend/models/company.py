from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    """
    Company model for storing target companies.
    
    This model represents companies that the user is targeting for job applications.
    It maintains relationships with contacts and applications at that company.
    """
    __tablename__ = 'companies'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Company information
    name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    contacts = db.relationship('Contact', backref='company', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='company', lazy='dynamic', cascade='all, delete-orphan')
    outreach_activities = db.relationship('OutreachActivity', backref='company', lazy='dynamic')

    def to_dict(self, include_related=False):
        """
        Convert company to dictionary for API responses.
        
        Args:
            include_related (bool): Whether to include counts of related records
            
        Returns:
            dict: Company data as dictionary
        """
        company_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'website': self.website,
            'location': self.location,
            'industry': self.industry,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_related:
            company_dict['contacts_count'] = self.contacts.count()
            company_dict['applications_count'] = self.applications.count()

        return company_dict

    def __repr__(self):
        return f'<Company {self.name}>'
