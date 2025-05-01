from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from scrapegod.utils import jwt_or_api_key_required
from scrapegod.extensions import db, csrf
from scrapegod.blueprints.scraper.models import Scraper
from scrapegod.blueprints.user.models import User  # Adjust the import path as needed
from scrapegod.blueprints.scraper.decorators import role_required  # Import the decorator


scraper = Blueprint('scraper', __name__, url_prefix='/scraper')

# Create a new scraper (restricted to admin and staff)
@scraper.route('/create', methods=['POST'])
@jwt_or_api_key_required  # Allow both JWT and API key authentication
@csrf.exempt  # Exempt from CSRF protection for API endpoints
def create_scraper(current_user):
    data = request.get_json()
    try:
        scraper = Scraper(
            name=data['name'],
            description=data.get('description'),
            lambda_link=data['lambda_link'],
            status=data.get('status', 'active'),
        )
        db.session.add(scraper)
        db.session.commit()
        return jsonify({'message': 'Scraper created successfully', 'scraper': scraper.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Update a scraper (restricted to admin and staff)
@scraper.route('/update/<int:scraper_id>', methods=['PUT'])
@jwt_or_api_key_required  # Ensure the user is authenticated
@csrf.exempt  # Exempt from CSRF protection for API endpoints
def update_scraper(current_user, scraper_id):
    data = request.get_json()
    scraper = Scraper.query.get_or_404(scraper_id)
    print(f"Scraper found: {scraper}")
    try:
        scraper.name = data.get('name', scraper.name)
        scraper.description = data.get('description', scraper.description)
        scraper.lambda_link = data.get('lambda_link', scraper.lambda_link)
        scraper.status = data.get('status', scraper.status)
        db.session.commit()
        return jsonify({'message': 'Scraper updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Delete a scraper (restricted to admin and staff)
@scraper.route('/delete/<int:scraper_id>', methods=['DELETE'])
@jwt_or_api_key_required  # Ensure the user is authenticated
@csrf.exempt  # Exempt from CSRF protection for API endpoints
def delete_scraper(current_user, scraper_id):
    scraper = Scraper.query.get_or_404(scraper_id)
    try:
        db.session.delete(scraper)
        db.session.commit()
        return jsonify({'message': 'Scraper deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# List all scrapers (accessible to all users)
@scraper.route('/scrapers', methods=['GET'])
@jwt_or_api_key_required  # Ensure the user is authenticated
@csrf.exempt  # Exempt from CSRF protection for API endpoints
def list_scrapers(current_user):
    scrapers = Scraper.query.all()
    return jsonify([
        {
            'id': scraper.id,
            'name': scraper.name,
            'description': scraper.description,
            'lambda_link': scraper.lambda_link,
            'status': scraper.status,
        }
        for scraper in scrapers
    ])