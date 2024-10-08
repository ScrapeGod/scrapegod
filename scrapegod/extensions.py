# from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail

# from flask_rest_jsonapi import Api
from flask_restful import Api as FlaskRestfulApi
from flask_sitemap import Sitemap
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf import CSRFProtect
from flask_argon2 import Argon2
from config import settings
from config.settings import REDIS_URL
from lib.sqlalchemy_base_class import ScrapegodModelBaseClass

# from flask_api_key import APIKeyManager

# debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy(model_class=ScrapegodModelBaseClass)
# api = Api()
flask_restful_api = FlaskRestfulApi(decorators=[csrf.exempt])
login_manager = LoginManager()
argon2 = Argon2()
# cors = CORS(supports_credentials=True, origins=['http://localhost:3000/'])
cors = CORS()
ext = Sitemap()
flask_static_digest = FlaskStaticDigest()
jwt = JWTManager()
cache = Cache(
    config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": REDIS_URL,
        "CACHE_THRESHOLD": settings.CACHE_THRESHOLD,
    }
)
