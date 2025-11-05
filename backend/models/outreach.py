from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OutreachActivity(db.Model):
    """
    Outreach activity model for tracking direct reach-out communications.
    
    This model tracks when and how the user reaches out to contacts at companies.
    Each outreach must be linked to either an application OR a company (not both).
    """
    __tablename__ = 'outreach_activities'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=True, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True, index=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False, index=True)

    # Outreach information
    channel = db.Column(db.String(50), nullable=False)  # 'Email' or 'LinkedIn'
    message_template = db.Column(db.Text)  # The message sent
    sent_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    follow_up_date = db.Column(db.DateTime)  # When to follow up
    status = db.Column(db.String(50), default='Sent')  # 'Sent', 'Responded', 'No Response'

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Critical Constraint: Exactly one of (application_id, company_id) must be non-NULL
    __table_args__ = (
        db.CheckConstraint(
            '(application_id IS NOT NULL AND company_id IS NULL) OR (application_id IS NULL AND company_id IS NOT NULL)',
            name='check_outreach_link'
        ),
    )

    def to_dict(self, include_related=False):
        """
        Convert outreach activity to dictionary for API responses.
        
        Args:
            include_related (bool): Whether to include related object details
            
        Returns:
            dict: Outreach activity data as dictionary
        """
        outreach_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'application_id': self.application_id,
            'company_id': self.company_id,
            'contact_id': self.contact_id,
            'channel': self.channel,
            'message_template': self.message_template,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_related:
            if self.contact:
                outreach_dict['contact'] = self.contact.to_dict()
            if self.application:
                outreach_dict['application'] = self.application.to_dict()
            if self.company:
                outreach_dict['company'] = self.company.to_dict()

        return outreach_dict

    def __repr__(self):
        return f'<OutreachActivity {self.channel} to {self.contact.name if self.contact else "Unknown"}>'
