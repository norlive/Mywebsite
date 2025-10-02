from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.portfolio import PortfolioItem
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in {'png', 'jpg', 'jpeg', 'gif'}:
        return 'image'
    elif ext in {'mp4', 'avi', 'mov', 'webm'}:
        return 'video'
    return 'unknown'

portfolio_bp = Blueprint('portfolio', __name__)

# Secret admin ID for authentication
ADMIN_SECRET_ID = 'BBA-ADMIN-LOGIN'

@portfolio_bp.route('/portfolio', methods=['GET'])
def get_portfolio_items():
    """Get all portfolio items"""
    try:
        items = PortfolioItem.query.all()
        return jsonify({
            'portfolio': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route("/portfolio", methods=["POST"])
def add_portfolio_item():
    """Add one or more new portfolio items (requires admin authentication)"""
    try:
        data = request.get_json()
        
        # Check admin authentication
        admin_id = data.get("admin_id")
        if admin_id != ADMIN_SECRET_ID:
            return jsonify({"error": "Unauthorized"}), 401
        
        items_data = data.get("items")
        if not isinstance(items_data, list):
            return jsonify({"error": "'items' must be a list"}), 400

        added_items = []
        for item_data in items_data:
            new_item = PortfolioItem(
                title=item_data.get("title"),
                src=item_data.get("src"),
                type=item_data.get("type"),
                category=item_data.get("category"),
                description=item_data.get("description", "")
            )
            db.session.add(new_item)
            added_items.append(new_item.to_dict())
        
        db.session.commit()
        
        return jsonify({
            "message": "Items added successfully",
            "items": added_items
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@portfolio_bp.route('/portfolio/<int:item_id>', methods=['DELETE'])
def delete_portfolio_item(item_id):
    """Delete a portfolio item (requires admin authentication)"""
    try:
        data = request.get_json()
        
        # Check admin authentication
        admin_id = data.get('admin_id')
        if admin_id != ADMIN_SECRET_ID:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Find and delete the item
        item = PortfolioItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Verify admin login"""
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        if admin_id == ADMIN_SECRET_ID:
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid Admin ID'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

