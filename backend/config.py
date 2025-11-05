import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with common settings"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Database settings
    # Fix Render's postgres:// to postgresql://
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///jobbuddy.db')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = FLASK_ENV == 'development' # Log SQL queries in dev

    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # File upload settings
    MAX_UPLOAD_MB = int(os.getenv('MAX_UPLOAD_MB', 2))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024 # Convert MB to bytes
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    UPLOAD_FOLDER = 'uploads'

    # CORS settings
    CORS_ORIGINS = os.getenv('FRONTEND_URL', 'http://localhost:3000').split(',')

    # External API settings
    HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', 'placeholder_hunter_api_key')
    ATS_API_KEY = os.getenv('ATS_API_KEY', 'placeholder_ats_api_key')
    ATS_API_URL = os.getenv('ATS_API_URL', 'https://ats-api.example.com')

    # Flask-Bcrypt
    BCRYPT_LOG_ROUNDS = 12

class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
