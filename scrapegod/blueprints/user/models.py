from scrapegod.extensions import login_manager, db, argon2
from flask_login import UserMixin
from lib.util_sqlalchemy import ResourceMixin
import secrets
import uuid


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class APIKey(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(
        db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
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
    api_keys = db.relationship("APIKey", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @classmethod
    def encrypt_password(cls, plaintext_password):

        if plaintext_password:
            return argon2.generate_password_hash(plaintext_password)

        return None

    def generate_api_key(self):
        """Generate a new API key for the user and save its hash."""
        # Generate a random API key
        api_key = secrets.token_urlsafe(32)

        # Hash the API key using argon2
        hashed_key = argon2.generate_password_hash(api_key)

        # Save the hashed key to the database
        api_key_entry = APIKey(user_id=self.id, key=hashed_key)
        db.session.add(api_key_entry)
        db.session.commit()

        # Return the plain key (to be shown only once to the user)
        return api_key

    @classmethod
    def create_user(cls, username, email, password):
        """Create a new user and generate an API key."""
        user = cls(
            username=username, email=email, password=cls.encrypt_password(password)
        )
        db.session.add(user)
        db.session.commit()
        return user
