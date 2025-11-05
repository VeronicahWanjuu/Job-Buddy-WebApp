"""
Applications routes for the JobBuddy API.

This module handles job application tracking with Kanban board functionality.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
import csv
import io
from models import db
from models.application import Application
from models.company import Company
from models.goal import Goal
from models.notification import Notification
from utils.validators import validate_job_title
from utils.error_handlers import APIError
from utils.decorators import login_required

# Create Blueprint for applications routes
applications_bp = Blueprint('applications', __name__, url_prefix='/api/v1/applications')


@applications_bp.route('', methods=['GET'])
@login_required
def list_applications():
    """
    Get all applications for the current user.
    
    Query parameters:
    - status: Filter by status (Planned, Applied, Interview, Offer, Rejected)
    - company_id: Filter by company
    - search: Search by job title or company name
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
        JSON with list of applications and pagination info
    """
    try:
        user_id = request.user_id
        
        # Get query parameters
        status = request.args.get('status', '').strip()
        company_id = request.args.get('company_id', type=int)
        search = request.args.get('search', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Application.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if company_id:
            query = query.filter_by(company_id=company_id)
        
        if search:
            query = query.filter(Application.job_title.ilike(f'%{search}%'))
        
        # Order by created_at descending
        query = query.order_by(Application.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        applications = [app.to_dict(include_company=True) for app in paginated.items]
        
        return jsonify({
            'applications': applications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
        
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@applications_bp.route('', methods=['POST'])
@login_required
def create_application():
    """
    Create a new application.
    
    Request body:
    {
        "company_id": 1,
        "job_title": "Senior Software Engineer",
        "job_url": "https://example.com/jobs/123",
        "status": "Planned",
        "notes": "Great opportunity"
    }
    
    Returns:
        JSON with created application data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data or not data.get('company_id') or not data.get('job_title'):
            raise APIError('Company ID and job title are required', 400)
        
        company_id = data.get('company_id')
        job_title = validate_job_title(data.get('job_title'))
        
        # Verify company exists and belongs to user
        company = Company.query.filter_by(id=company_id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        # Create application
        status = data.get('status', 'Planned')
        valid_statuses = ['Planned', 'Applied', 'Interview', 'Offer', 'Rejected']
        if status not in valid_statuses:
            status = 'Planned'
        
        application = Application(
            user_id=user_id,
            company_id=company_id,
            job_title=job_title,
            job_url=data.get('job_url', '').strip() or None,
            status=status,
            applied_date=datetime.utcnow().date() if status == 'Applied' else None,
            notes=data.get('notes', '').strip() or None
        )
        
        db.session.add(application)
        db.session.flush()
        
        # If status is Applied, create follow-up notification
        if status == 'Applied':
            follow_up_date = datetime.utcnow() + timedelta(days=3)
            notification = Notification(
                user_id=user_id,
                type='follow_up',
                title='Follow up on application',
                message=f'Remember to follow up on your application to {company.name} for {job_title}',
                related_type='application',
                related_id=application.id
            )
            db.session.add(notification)
            
            # Increment weekly goal counter
            today = datetime.utcnow().date()
            week_start = today - timedelta(days=today.weekday())
            goal = Goal.query.filter_by(user_id=user_id, week_start=week_start).first()
            if goal:
                goal.applications_current += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Application created successfully',
            'application': application.to_dict(include_company=True)
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@applications_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_application(id):
    """
    Get a specific application.
    
    Returns:
        JSON with application data
    """
    try:
        user_id = request.user_id
        
        application = Application.query.filter_by(id=id, user_id=user_id).first()
        if not application:
            raise APIError('Application not found', 404)
        
        return jsonify({
            'application': application.to_dict(include_company=True)
        }), 200
        
    except APIError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@applications_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_application(id):
    """
    Update an application.
    
    Request body:
    {
        "job_title": "Senior Software Engineer",
        "status": "Applied",
        "notes": "Updated notes"
    }
    
    Returns:
        JSON with updated application data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        application = Application.query.filter_by(id=id, user_id=user_id).first()
        if not application:
            raise APIError('Application not found', 404)
        
        old_status = application.status
        
        # Update fields
        if 'job_title' in data:
            application.job_title = validate_job_title(data.get('job_title'))
        if 'job_url' in data:
            application.job_url = data.get('job_url', '').strip() or None
        if 'status' in data:
            new_status = data.get('status')
            valid_statuses = ['Planned', 'Applied', 'Interview', 'Offer', 'Rejected']
            if new_status in valid_statuses:
                application.status = new_status
                
                # If status changed to Applied, set applied_date and create notification
                if old_status != 'Applied' and new_status == 'Applied':
                    application.applied_date = datetime.utcnow().date()
                    
                    notification = Notification(
                        user_id=user_id,
                        type='follow_up',
                        title='Follow up on application',
                        message=f'Remember to follow up on your application to {application.company.name} for {application.job_title}',
                        related_type='application',
                        related_id=application.id
                    )
                    db.session.add(notification)
                    
                    # Increment weekly goal counter
                    today = datetime.utcnow().date()
                    week_start = today - timedelta(days=today.weekday())
                    goal = Goal.query.filter_by(user_id=user_id, week_start=week_start).first()
                    if goal:
                        goal.applications_current += 1
        
        if 'notes' in data:
            application.notes = data.get('notes', '').strip() or None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Application updated successfully',
            'application': application.to_dict(include_company=True)
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@applications_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_application(id):
    """
    Delete an application.
    
    Returns:
        JSON success message
    """
    try:
        user_id = request.user_id
        
        application = Application.query.filter_by(id=id, user_id=user_id).first()
        if not application:
            raise APIError('Application not found', 404)
        
        db.session.delete(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Application deleted successfully'
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@applications_bp.route('/bulk-upload', methods=['POST'])
@login_required
def bulk_upload_applications():
    """
    Bulk upload applications from CSV file.
    
    CSV format:
    company_name,job_title,job_url,status,notes
    
    Returns:
        JSON with upload results
    """
    try:
        user_id = request.user_id
        
        if 'file' not in request.files:
            raise APIError('No file provided', 400)
        
        file = request.files['file']
        if not file or file.filename == '':
            raise APIError('No file selected', 400)
        
        if not file.filename.endswith('.csv'):
            raise APIError('File must be CSV format', 400)
        
        # Read CSV
        stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
        csv_reader = csv.DictReader(stream)
        
        successful = 0
        failed = 0
        errors = []
        
        for row in csv_reader:
            try:
                company_name = row.get('company_name', '').strip()
                job_title = validate_job_title(row.get('job_title', ''))
                
                if not company_name:
                    failed += 1
                    errors.append('Company name is required')
                    continue
                
                # Find or create company
                company = Company.query.filter_by(user_id=user_id, name=company_name).first()
                if not company:
                    company = Company(user_id=user_id, name=company_name)
                    db.session.add(company)
                    db.session.flush()
                
                # Create application
                status = row.get('status', 'Planned')
                valid_statuses = ['Planned', 'Applied', 'Interview', 'Offer', 'Rejected']
                if status not in valid_statuses:
                    status = 'Planned'
                
                application = Application(
                    user_id=user_id,
                    company_id=company.id,
                    job_title=job_title,
                    job_url=row.get('job_url', '').strip() or None,
                    status=status,
                    applied_date=datetime.utcnow().date() if status == 'Applied' else None,
                    notes=row.get('notes', '').strip() or None
                )
                
                db.session.add(application)
                successful += 1
                
            except Exception as e:
                failed += 1
                errors.append(str(e))
        
        db.session.commit()
        
        return jsonify({
            'message': f'Bulk upload completed: {successful} successful, {failed} failed',
            'successful': successful,
            'failed': failed,
            'errors': errors
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
