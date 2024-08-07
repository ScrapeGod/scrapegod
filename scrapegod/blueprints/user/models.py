from scrapegod.extensions import login_manager, db
from datetime import datetime
from flask_login import UserMixin
from lib.util_sqlalchemy import ResourceMixin
from werkzeug.security import generate_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True)
    email = db.Column(db.String(255), nullable=False, server_default="")
    password = db.Column(db.String(128), nullable=False, server_default="")
    

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
            return generate_password_hash(plaintext_password)

        return None