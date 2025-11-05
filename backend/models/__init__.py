from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database and migration engine."""
    db.init_app(app)
    migrate.init_app(app, db)

# Import all models here so they are registered with SQLAlchemy
from .user import User
from .onboarding import OnboardingData
from .company import Company
from .contact import Contact
from .application import Application
from .outreach import OutreachActivity
from .cv_analysis import CVAnalysis
from .goal import Goal
from .streak import Streak
from .notification import Notification
