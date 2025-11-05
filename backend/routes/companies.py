"""
Companies routes for the JobBuddy API.

This module handles company management operations.
"""

from flask import Blueprint, request, jsonify
from models import db
from models.company import Company
from models.contact import Contact
from utils.error_handlers import APIError
from utils.decorators import login_required, owner_required

# Create Blueprint for companies routes
companies_bp = Blueprint('companies', __name__, url_prefix='/api/v1/companies')


@companies_bp.route('', methods=['GET'])
@login_required
def list_companies():
    """
    Get all companies for the current user.
    
    Query parameters:
    - search: Search by company name
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
        JSON with list of companies and pagination info
    """
    try:
        user_id = request.user_id
        
        # Get query parameters
        search = request.args.get('search', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Company.query.filter_by(user_id=user_id)
        
        if search:
            query = query.filter(Company.name.ilike(f'%{search}%'))
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        companies = [company.to_dict(include_related=True) for company in paginated.items]
        
        return jsonify({
            'companies': companies,
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


@companies_bp.route('', methods=['POST'])
@login_required
def create_company():
    """
    Create a new company.
    
    Request body:
    {
        "name": "Google",
        "website": "https://google.com",
        "location": "Mountain View, CA",
        "industry": "Technology",
        "notes": "Dream company"
    }
    
    Returns:
        JSON with created company data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data or not data.get('name'):
            raise APIError('Company name is required', 400)
        
        # Create company
        company = Company(
            user_id=user_id,
            name=data.get('name', '').strip(),
            website=data.get('website', '').strip() or None,
            location=data.get('location', '').strip() or None,
            industry=data.get('industry', '').strip() or None,
            notes=data.get('notes', '').strip() or None
        )
        
        db.session.add(company)
        db.session.commit()
        
        return jsonify({
            'message': 'Company created successfully',
            'company': company.to_dict()
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@companies_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_company(id):
    """
    Get a specific company with its contacts.
    
    Returns:
        JSON with company data and related contacts
    """
    try:
        user_id = request.user_id
        
        company = Company.query.filter_by(id=id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        # Get contacts for this company
        contacts = Contact.query.filter_by(company_id=id).all()
        contacts_data = [contact.to_dict() for contact in contacts]
        
        company_data = company.to_dict(include_related=True)
        company_data['contacts'] = contacts_data
        
        return jsonify({
            'company': company_data
        }), 200
        
    except APIError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@companies_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_company(id):
    """
    Update a company.
    
    Request body:
    {
        "name": "Google Inc",
        "website": "https://google.com",
        "location": "Mountain View, CA",
        "industry": "Technology",
        "notes": "Dream company"
    }
    
    Returns:
        JSON with updated company data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        company = Company.query.filter_by(id=id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        # Update fields
        if 'name' in data:
            company.name = data.get('name', '').strip()
        if 'website' in data:
            company.website = data.get('website', '').strip() or None
        if 'location' in data:
            company.location = data.get('location', '').strip() or None
        if 'industry' in data:
            company.industry = data.get('industry', '').strip() or None
        if 'notes' in data:
            company.notes = data.get('notes', '').strip() or None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Company updated successfully',
            'company': company.to_dict()
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@companies_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_company(id):
    """
    Delete a company and all its related data.
    
    Returns:
        JSON success message
    """
    try:
        user_id = request.user_id
        
        company = Company.query.filter_by(id=id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        db.session.delete(company)
        db.session.commit()
        
        return jsonify({
            'message': 'Company deleted successfully'
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
