"""
Custom decorators for the JobBuddy API.

This module provides decorators for authentication, authorization, and other
cross-cutting concerns.
"""

from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from .error_handlers import APIError
from models.user import User


def login_required(f):
    """
    Decorator to require JWT authentication.
    
    This decorator verifies that a valid JWT token is present in the request
    and that the user still exists in the database.
    
    Args:
        f: Flask route function to decorate
        
    Returns:
        Decorated function that requires authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            
            # Get user ID from token
            user_id = get_jwt_identity()
            
            # Verify user still exists
            user = User.query.get(user_id)
            if not user:
                raise APIError('User not found', 404)
            
            # Add user_id to request context for use in route
            request.user_id = user_id
            request.current_user = user
            
        except Exception as e:
            if isinstance(e, APIError):
                raise
            raise APIError('Invalid or missing authentication token', 401)
        
        return f(*args, **kwargs)
    
    return decorated_function


def owner_required(resource_type):
    """
    Decorator to verify user owns the resource.
    
    This decorator checks that the authenticated user owns the resource
    they are trying to access or modify.
    
    Args:
        resource_type (str): Type of resource ('application', 'company', etc.)
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the resource ID from URL parameters
            resource_id = kwargs.get('id')
            if not resource_id:
                raise APIError('Resource ID not provided', 400)
            
            # Get the current user (assumes login_required is applied first)
            user_id = getattr(request, 'user_id', None)
            if not user_id:
                raise APIError('Authentication required', 401)
            
            # Import model dynamically to avoid circular imports
            if resource_type == 'application':
                from models.application import Application
                resource = Application.query.get(resource_id)
            elif resource_type == 'company':
                from models.company import Company
                resource = Company.query.get(resource_id)
            elif resource_type == 'contact':
                from models.contact import Contact
                resource = Contact.query.get(resource_id)
            elif resource_type == 'outreach':
                from models.outreach import OutreachActivity
                resource = OutreachActivity.query.get(resource_id)
            elif resource_type == 'cv_analysis':
                from models.cv_analysis import CVAnalysis
                resource = CVAnalysis.query.get(resource_id)
            else:
                raise APIError('Unknown resource type', 400)
            
            # Check if resource exists
            if not resource:
                raise APIError(f'{resource_type.capitalize()} not found', 404)
            
            # Check if user owns the resource
            if resource.user_id != user_id:
                raise APIError('You do not have permission to access this resource', 403)
            
            # Add resource to request context
            setattr(request, resource_type, resource)
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
