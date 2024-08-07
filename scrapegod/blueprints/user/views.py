from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from scrapegod.blueprints.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from scrapegod.blueprints.user.models import User
from scrapegod import app
from scrapegod.extensions import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

user = Blueprint('user', __name__)

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered sucessfully"), 201

@app.route("/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401
        

