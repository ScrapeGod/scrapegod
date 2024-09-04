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
    User.create_user(username=data['username'], email=data['email'], password=data['password'])
    return jsonify(message="User registered sucessfully"), 201

@user.route("/login", methods=['GET', 'POST'])
@csrf.exempt
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        response = jsonify({'message': 'Login successful'})
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=False, samesite='Lax')
        return response
    return jsonify(message="Invalid credentials"), 401

@user.route('/logout', methods=['POST'])
@jwt_required()
@csrf.exempt
def logout():
    response = jsonify({'message': 'Logout successful'})
    
    # Remove the cookie by setting it with an expiration date in the past
    response.set_cookie('access_token_cookie', '', expires=0, httponly=True, secure=False, samesite='Lax')
    
    return response

@user.route('/update', methods=['PUT'])
@jwt_required()
@csrf.exempt
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
@csrf.exempt
def get_user_info():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200
