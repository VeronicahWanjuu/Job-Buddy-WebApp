"""
Error handling utilities for the JobBuddy API.

This module provides standardized error responses and custom exception classes
for consistent error handling across the application.
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """
    Custom exception for API errors.
    
    Attributes:
        message (str): Error message
        code (str): Error code for client handling
        status_code (int): HTTP status code
    """
    def __init__(self, message, status_code=400, code=None):
        self.message = message
        self.status_code = status_code
        self.code = code or self._get_default_code(status_code)

    def _get_default_code(self, status_code):
        """Map HTTP status code to error code."""
        status_code_map = {
            400: 'BAD_REQUEST',
            401: 'UNAUTHORIZED',
            403: 'FORBIDDEN',
            404: 'NOT_FOUND',
            408: 'TIMEOUT',
            413: 'FILE_TOO_LARGE',
            422: 'INVALID_DATA_FORMAT',
            429: 'RATE_LIMIT_EXCEEDED',
            500: 'INTERNAL_SERVER_ERROR',
            503: 'SERVICE_UNAVAILABLE'
        }
        return status_code_map.get(status_code, 'UNKNOWN_ERROR')

    def to_dict(self):
        """Convert error to dictionary for JSON response."""
        return {
            'error': {
                'code': self.code,
                'message': self.message
            }
        }


def register_error_handlers(app):
    """
    Register error handlers with the Flask app.
    
    Args:
        app: Flask application instance
    """

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP exceptions."""
        api_error = APIError(error.description, error.code)
        response = jsonify(api_error.to_dict())
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle generic exceptions."""
        api_error = APIError('An unexpected error occurred', 500)
        response = jsonify(api_error.to_dict())
        response.status_code = 500
        return response
