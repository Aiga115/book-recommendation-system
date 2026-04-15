from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'message': 'Access denied!'}), 403

    return jsonify({'message': f"Welcome Admin!"}), 200