"""
JobBuddy Flask Application

This is the main entry point for the JobBuddy backend API.
It initializes the Flask app, database, JWT, CORS, and registers all routes.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from models import db, migrate, init_db
from utils.error_handlers import register_error_handlers

# Import routes
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.onboarding import onboarding_bp
from routes.companies import companies_bp
from routes.contacts import contacts_bp
from routes.applications import applications_bp
from routes.goals import goals_bp
from routes.notifications import notifications_bp


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize database
    init_db(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(notifications_bp)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/api/v1/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'message': 'JobBuddy API is running'
        }), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
