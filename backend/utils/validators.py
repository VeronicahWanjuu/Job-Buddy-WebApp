"""
Validation utilities for the JobBuddy API.

This module provides validation functions for common input types and constraints.
"""

import re
from .error_handlers import APIError


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Raises:
        APIError: If email format is invalid
        
    Returns:
        str: Valid email address
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise APIError('Invalid email format', 400, 'INVALID_EMAIL')
    return email


def validate_password(password):
    """
    Validate password strength.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Args:
        password (str): Password to validate
        
    Raises:
        APIError: If password doesn't meet requirements
        
    Returns:
        str: Valid password
    """
    if len(password) < 8:
        raise APIError('Password must be at least 8 characters long', 400, 'WEAK_PASSWORD')
    
    if not re.search(r'[A-Z]', password):
        raise APIError('Password must contain at least one uppercase letter', 400, 'WEAK_PASSWORD')
    
    if not re.search(r'[a-z]', password):
        raise APIError('Password must contain at least one lowercase letter', 400, 'WEAK_PASSWORD')
    
    if not re.search(r'\d', password):
        raise APIError('Password must contain at least one digit', 400, 'WEAK_PASSWORD')
    
    return password


def validate_job_title(job_title):
    """
    Validate job title.
    
    Requirements:
    - Minimum 3 characters
    
    Args:
        job_title (str): Job title to validate
        
    Raises:
        APIError: If job title is invalid
        
    Returns:
        str: Valid job title
    """
    if not job_title or len(job_title.strip()) < 3:
        raise APIError('Job title must be at least 3 characters long', 400, 'INVALID_JOB_TITLE')
    
    return job_title.strip()


def validate_url(url):
    """
    Validate URL format.
    
    Args:
        url (str): URL to validate
        
    Raises:
        APIError: If URL format is invalid
        
    Returns:
        str: Valid URL
    """
    url_regex = r'^https?://[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise APIError('Invalid URL format', 400, 'INVALID_URL')
    
    return url


def validate_file_type(filename, allowed_extensions):
    """
    Validate file extension.
    
    Args:
        filename (str): Name of file to validate
        allowed_extensions (set): Set of allowed file extensions
        
    Raises:
        APIError: If file type is not allowed
        
    Returns:
        str: File extension
    """
    if '.' not in filename:
        raise APIError('File must have an extension', 400, 'INVALID_FILE')
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        raise APIError(f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}', 400, 'INVALID_FILE_TYPE')
    
    return ext


def validate_file_size(file_size, max_size_mb):
    """
    Validate file size.
    
    Args:
        file_size (int): Size of file in bytes
        max_size_mb (int): Maximum allowed size in MB
        
    Raises:
        APIError: If file is too large
        
    Returns:
        int: File size in bytes
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise APIError(f'File size exceeds maximum of {max_size_mb}MB', 413, 'FILE_TOO_LARGE')
    
    return file_size
