from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from db import db

auth_bp = Blueprint('auth', __name__)
bcrypt  = Bcrypt()

# ─── REGISTER ────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    # Hash the password
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username = data['username'],
        email    = data['email'],
        password = hashed_pw,
        role     = data.get('role', 'user')  # default is 'user'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


# ─── LOGIN ────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Create JWT token with role inside
    token = create_access_token(identity={
        'id'  : user.id,
        'role': user.role
    })

    return jsonify({
        'message': 'Login successful!',
        'token'  : token,
        'role'   : user.role
    }), 200