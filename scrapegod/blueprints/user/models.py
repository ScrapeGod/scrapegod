from scrapegod.extensions import login_manager, db, bcrypt
from datetime import datetime
from flask_login import UserMixin
from lib.util_sqlalchemy import ResourceMixin
from werkzeug.security import generate_password_hash
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class APIKey(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revoked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"APIKey('{self.key}', User ID: '{self.user_id}')"
    
    def revoke(self):
        """Mark the API key as revoked."""
        self.revoked = True
        db.session.commit()
    
class User(db.Model, UserMixin, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True)
    email = db.Column(db.String(255), nullable=False, server_default="", unique=True)
    password = db.Column(db.String(128), nullable=False, server_default="")
    api_keys = db.relationship('APIKey', backref='user', lazy=True)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

        return None
    
    
    def generate_api_key(self):
        """Generate a new API key for the user."""
        api_key = APIKey(user_id=self.id)
        db.session.add(api_key)
        db.session.commit()
        return api_key.key

    @classmethod
    def create_user(cls, username, email, password):
        """Create a new user and generate an API key."""
        user = cls(username=username, email=email, password=cls.encrypt_password(password))
        db.session.add(user)
        db.session.commit()
        user.generate_api_key()  # Generate an API key after creating the user
        return user
    

    