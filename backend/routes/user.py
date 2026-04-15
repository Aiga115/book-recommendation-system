from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    current_user = get_jwt_identity()

    if current_user['role'] != 'user':
        return jsonify({'message': 'Access denied!'}), 403

    return jsonify({'message': 'Welcome User!'}), 200