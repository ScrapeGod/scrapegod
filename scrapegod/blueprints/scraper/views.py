from flask import Blueprint, request, jsonify
from scrapegod.extensions import db, csrf
from scrapegod.blueprints.scraper.models import Scraper
from scrapegod.blueprints.user.models import User  # Adjust the import path as needed
from scrapegod.blueprints.scraper.decorators import role_required  # Import the decorator

scraper = Blueprint('scraper', __name__, url_prefix='/scrapers')

# Create a new scraper (restricted to admin and staff)
@scraper.route('/', methods=['POST'])
@csrf.exempt  # Exempt from CSRF protection for API endpoints
def create_scraper():
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
@scraper.route('/<int:scraper_id>', methods=['PUT'])
@role_required('admin', 'staff')
def update_scraper(scraper_id):
    data = request.get_json()
    scraper = Scraper.query.get_or_404(scraper_id)
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
@scraper.route('/<int:scraper_id>', methods=['DELETE'])
@role_required('admin', 'staff')
def delete_scraper(scraper_id):
    scraper = Scraper.query.get_or_404(scraper_id)
    try:
        db.session.delete(scraper)
        db.session.commit()
        return jsonify({'message': 'Scraper deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# List all scrapers (accessible to all users)
@scraper.route('/', methods=['GET'])
def list_scrapers():
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