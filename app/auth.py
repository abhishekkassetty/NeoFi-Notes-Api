from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already taken'}), 409

    new_user = User(username=username, email=email, password=generate_password_hash(password, method="pbkdf2:sha256"))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, username=user.username, email=user.email), 200
    else:
        return jsonify({'error': 'Invalid username/email or password'}), 401
