from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    """
    Contact model for storing contacts at target companies.
    
    This model represents individual contacts (people) at companies that the user
    wants to reach out to. Contacts can be discovered via API or added manually.
    """
    __tablename__ = 'contacts'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Contact information
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    role = db.Column(db.String(255))
    source = db.Column(db.String(50))  # 'API' (from Hunter.io) or 'Manual' (user added)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    outreach_activities = db.relationship('OutreachActivity', backref='contact', lazy='dynamic')

    # Unique constraint: same email can't exist twice for same company
    __table_args__ = (
        db.UniqueConstraint('company_id', 'email', name='unique_company_email'),
    )

    def to_dict(self):
        """
        Convert contact to dictionary for API responses.
        
        Returns:
            dict: Contact data as dictionary
        """
        return {
            'id': self.id,
            'company_id': self.company_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'linkedin_url': self.linkedin_url,
            'role': self.role,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Contact {self.name}>'
