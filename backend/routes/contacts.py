"""
Contacts routes for the JobBuddy API.

This module handles contact management operations including manual entry
and Hunter.io API integration for contact discovery.
"""

from flask import Blueprint, request, jsonify
import requests
from models import db
from models.contact import Contact
from models.company import Company
from utils.error_handlers import APIError
from utils.decorators import login_required
from config import get_config

# Create Blueprint for contacts routes
contacts_bp = Blueprint('contacts', __name__, url_prefix='/api/v1/contacts')

config = get_config()


@contacts_bp.route('', methods=['GET'])
@login_required
def list_contacts():
    """
    Get all contacts for the current user.
    
    Query parameters:
    - company_id: Filter by company
    - search: Search by contact name or email
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
        JSON with list of contacts and pagination info
    """
    try:
        user_id = request.user_id
        
        # Get query parameters
        company_id = request.args.get('company_id', type=int)
        search = request.args.get('search', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Contact.query.filter_by(user_id=user_id)
        
        if company_id:
            query = query.filter_by(company_id=company_id)
        
        if search:
            query = query.filter(
                (Contact.name.ilike(f'%{search}%')) | 
                (Contact.email.ilike(f'%{search}%'))
            )
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        contacts = [contact.to_dict() for contact in paginated.items]
        
        return jsonify({
            'contacts': contacts,
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


@contacts_bp.route('', methods=['POST'])
@login_required
def create_contact():
    """
    Create a new contact manually.
    
    Request body:
    {
        "company_id": 1,
        "name": "John Doe",
        "email": "john@google.com",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "role": "Engineering Manager"
    }
    
    Returns:
        JSON with created contact data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data or not data.get('company_id') or not data.get('name'):
            raise APIError('Company ID and name are required', 400)
        
        company_id = data.get('company_id')
        
        # Verify company exists and belongs to user
        company = Company.query.filter_by(id=company_id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        # Check for duplicate email in same company
        email = data.get('email', '').strip() or None
        if email:
            existing = Contact.query.filter_by(company_id=company_id, email=email).first()
            if existing:
                raise APIError('Contact with this email already exists for this company', 400)
        
        # Create contact
        contact = Contact(
            user_id=user_id,
            company_id=company_id,
            name=data.get('name', '').strip(),
            email=email,
            linkedin_url=data.get('linkedin_url', '').strip() or None,
            role=data.get('role', '').strip() or None,
            source='Manual'
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact created successfully',
            'contact': contact.to_dict()
        }), 201
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@contacts_bp.route('/discover', methods=['POST'])
@login_required
def discover_contacts():
    """
    Discover contacts via Hunter.io API.
    
    Request body:
    {
        "company_id": 1,
        "company_domain": "google.com"
    }
    
    Returns:
        JSON with discovered contacts or fallback message
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data or not data.get('company_id') or not data.get('company_domain'):
            raise APIError('Company ID and domain are required', 400)
        
        company_id = data.get('company_id')
        domain = data.get('company_domain', '').strip()
        
        # Verify company exists and belongs to user
        company = Company.query.filter_by(id=company_id, user_id=user_id).first()
        if not company:
            raise APIError('Company not found', 404)
        
        # Try Hunter.io API
        api_key = config.HUNTER_API_KEY
        if not api_key or api_key == 'placeholder_hunter_api_key':
            raise APIError('Hunter.io API key not configured. Please add contacts manually.', 503)
        
        try:
            # Call Hunter.io API
            response = requests.get(
                'https://api.hunter.io/v2/domain-search',
                params={
                    'domain': domain,
                    'limit': 10,
                    'api_key': api_key
                },
                timeout=10
            )
            
            if response.status_code == 401:
                raise APIError('Hunter.io API key is invalid', 503)
            elif response.status_code == 429:
                raise APIError('Hunter.io API quota exceeded. Please add contacts manually.', 429)
            elif response.status_code != 200:
                raise APIError('Hunter.io API error. Please add contacts manually.', 503)
            
            data = response.json()
            discovered_contacts = []
            
            # Process discovered contacts
            for person in data.get('data', {}).get('emails', []):
                email = person.get('value')
                
                # Check if contact already exists
                existing = Contact.query.filter_by(company_id=company_id, email=email).first()
                if existing:
                    continue
                
                # Create contact
                contact = Contact(
                    user_id=user_id,
                    company_id=company_id,
                    name=f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                    email=email,
                    role=person.get('position'),
                    source='API'
                )
                
                db.session.add(contact)
                discovered_contacts.append(contact.to_dict())
            
            db.session.commit()
            
            return jsonify({
                'message': f'Discovered {len(discovered_contacts)} contacts',
                'contacts': discovered_contacts
            }), 201
            
        except requests.exceptions.Timeout:
            raise APIError('Hunter.io API request timed out. Please try again later.', 408)
        except requests.exceptions.RequestException as e:
            raise APIError(f'Hunter.io API error: {str(e)}', 503)
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@contacts_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_contact(id):
    """
    Update a contact.
    
    Request body:
    {
        "name": "Jane Doe",
        "email": "jane@google.com",
        "linkedin_url": "https://linkedin.com/in/janedoe",
        "role": "Senior Engineer"
    }
    
    Returns:
        JSON with updated contact data
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        contact = Contact.query.filter_by(id=id, user_id=user_id).first()
        if not contact:
            raise APIError('Contact not found', 404)
        
        # Update fields
        if 'name' in data:
            contact.name = data.get('name', '').strip()
        if 'email' in data:
            contact.email = data.get('email', '').strip() or None
        if 'linkedin_url' in data:
            contact.linkedin_url = data.get('linkedin_url', '').strip() or None
        if 'role' in data:
            contact.role = data.get('role', '').strip() or None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Contact updated successfully',
            'contact': contact.to_dict()
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500


@contacts_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_contact(id):
    """
    Delete a contact.
    
    Returns:
        JSON success message
    """
    try:
        user_id = request.user_id
        
        contact = Contact.query.filter_by(id=id, user_id=user_id).first()
        if not contact:
            raise APIError('Contact not found', 404)
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact deleted successfully'
        }), 200
        
    except APIError as e:
        db.session.rollback()
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        db.session.rollback()
        error = APIError(str(e), 500)
        return jsonify(error.to_dict()), 500
