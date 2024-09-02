from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from scrapegod.blueprints.user.models import User
import jwt
from scrapegod import app
from scrapegod.extensions import db, bcrypt, csrf
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
user = Blueprint('user', __name__)

@user.route("/register", methods=['POST'])
@csrf.exempt
def register():
    data = request.get_json()
    # Check if the email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message="Email already in use"), 400
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print(data)
    return jsonify(message="User registered sucessfully"), 201

@user.route("/login", methods=['GET', 'POST'])
def login():
    print("hello")
    data = request.get_json()
    print(data)
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@user.route('/update', methods=['PUT'])
@jwt_required()
def update():
    data = request.get_json()
    user_identity = get_jwt_identity()
    user = User.query.filter_by(email=user_identity['email']).first()
    if user:
        user.username = data['username'] if 'username' in data else user.username
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if 'password' in data else user.password
        db.session.commit()
        return jsonify(message="User updated successfully"), 200
    return jsonify(message="User not found"), 404

@user.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200
        