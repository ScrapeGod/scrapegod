from lib.util_sqlalchemy import ResourceMixin
from sqlalchemy.dialects.postgresql import JSON
from scrapegod.extensions import db

class Scraper(ResourceMixin, db.Model):
    __tablename__ = 'scraper'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the scraper
    name = db.Column(db.String(128), nullable=False)  # Name of the scraper
    description = db.Column(db.Text, nullable=True)  # Description of the scraper
    lambda_link = db.Column(db.String(256), nullable=False)  # Link to the Lambda function
    status = db.Column(db.String(32), default='active')  # Status of the scraper (e.g., active, inactive)

    def __repr__(self):
        return f"<Scraper {self.name}>"