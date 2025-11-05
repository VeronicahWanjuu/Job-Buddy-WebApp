from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User model for authentication and profile management.
    
    This model stores user account information including email, password hash, and name.
    It maintains relationships with all other user-specific data models.
    """
    __tablename__ = 'users'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships (defined as we create other models)
    onboarding = db.relationship('OnboardingData', backref='user', uselist=False, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    companies = db.relationship('Company', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    outreach_activities = db.relationship('OutreachActivity', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cv_analyses = db.relationship('CVAnalysis', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    streak = db.relationship('Streak', backref='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """
        Hash and set user password using Werkzeug's security functions.
        
        Args:
            password (str): Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_stats=False):
        """
        Convert user object to dictionary for API responses.
        
        Args:
            include_stats (bool): Whether to include user statistics
            
        Returns:
            dict: User data as dictionary
        """
        user_dict = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_stats:
            # Add statistics if requested
            user_dict['stats'] = {
                'total_applications': self.applications.count(),
                'total_companies': self.companies.count(),
                'total_outreach': self.outreach_activities.count(),
                'total_cv_analyses': self.cv_analyses.count()
            }

        return user_dict

    def __repr__(self):
        return f'<User {self.email}>'
