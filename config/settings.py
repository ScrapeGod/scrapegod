import json
import os
from celery.schedules import crontab, timedelta
from dotenv import load_dotenv
import json
import os

env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

load_dotenv(env_file)

UPLOAD_FOLDER = os.path.abspath("data")


def if_none_false_env_bool_setting(key):
    value = os.getenv(key, None)
    if value is None:
        return False

    return value.lower() == "true"

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# SECRET_KEY = os.getenv('SECRET_KEY', None)
SECRET_KEY = os.getenv("SECRET_KEY", None)
# Add host.docker.internal as SERVER_NAME when testing with selenium locally

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{}".format(os.getenv("DOCKER_WEB_PORT", "8000"))
)

IO_DOMAIN = os.getenv(
    "IO_DOMAIN", "localhost:{}".format(os.getenv("DOCKER_WEB_PORT", "8000"))
)

CACHE_THRESHOLD = 8000
# SQLAlchemy.
SESSION_COOKIE_SECURE = False
pg_user = os.getenv("POSTGRES_USER", "postgres")
pg_pass = os.getenv("POSTGRES_PASSWORD", "password")
pg_host = os.getenv("POSTGRES_HOST", "postgres")
pg_port = os.getenv("POSTGRES_PORT", "5432")
pg_db = os.getenv("POSTGRES_DB", pg_user)
db = "postgresql://{}:{}@{}:{}/{}".format(pg_user, pg_pass, pg_host, pg_port, pg_db)
SQLALCHEMY_DATABASE_URI = db
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_POOL_OVERFLOW = 30


pg_port_pytest = os.getenv("PG_PORT_PYTEST", "5432")
pg_host_pytest = os.getenv("PG_HOST_PYTEST", "postgres")
SQLALCHEMY_TEST_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    pg_user, pg_pass, pg_host_pytest, pg_port_pytest, pg_db
)
if os.getenv("PYTEST_SESSION", False):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_TEST_DATABASE_URI

from kombu import Exchange, Queue


# Celery.
REDIS_URL = os.getenv("REDIS_URL", "redis://:splendidponchodesire@redis:6379/0")
CELERY_RESULT_BACKEND = "db+" + db
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_REDIS_MAX_CONNECTIONS = 10
CELERY_TASK_TIME_LIMIT = 3600  # 60 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 3600  # 60 minutes
# Setting UTC time so schedule happens 8am AEDT
if ".com" in SERVER_NAME:  # includes docker.host.internal
    CELERY_CONFIG = {
        "broker_url": REDIS_URL,
        "result_backend": CELERY_RESULT_BACKEND,
        "result_expires": 60 * 60,  # 1 hour expiration
        # "task_default_priority": 5,
        # "broker_transport_options": {
        #     "priority_steps": list(range(10)),
        #     "sep": ":",
        #     "queue_order_strategy": "priority",
        # },
        # "task_queues": [
        #     Queue("celery", Exchange("tasks"), queue_arguments={"x-max-priority": 10}),
        # ],
        "include": [
            #"scrapegod.blueprints.contact.tasks",
        ],
        
        "beat_schedule": {
        #     "create-scrapegod-bills-rodrigo": {
        #         "task": "scrapegod.blueprints.billing.tasks.create_scrapegod_bills",
        #         "schedule": crontab(hour=5, minute=0),
        #         "kwargs": {"uid": "bikash@scrapegod.com.au"},
        #     },
            
        },
    }


else:
    CELERY_CONFIG = {
        "broker_url": REDIS_URL,
        "result_backend": CELERY_RESULT_BACKEND,
        "result_expires": 60 * 60,  # 1 hour expiration
        # "task_default_priority": 5,
        # "broker_transport_options": {
        #     "priority_steps": list(range(10)),
        #     "sep": ":",
        #     "queue_order_strategy": "priority",
        # },
        # "task_queues": [
        #     Queue("celery", Exchange("tasks"), queue_arguments={"x-max-priority": 10}),
        # ],
        "include": [
            #"scrapegod.blueprints.contact.tasks",
        ],
        "beat_schedule": {},
    }

# User.
SEED_ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "dev@local.host")
SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "password")
REMEMBER_COOKIE_DURATION = timedelta(days=90)

XERO_CLIENT_ID = os.environ.get("XERO_CLIENT_ID")
XERO_SECRET = os.environ.get("XERO_SECRET")
XERO_REDIRECT_URI = os.environ.get("XERO_REDIRECT_URI")

# Flask-Mail.
# SEND INVOICE EMAIL
SEND_INVOICE_EMAIL = if_none_false_env_bool_setting("SEND_INVOICE_EMAIL")

# SEND_EMAIL only for local setting, not applied in production
SEND_EMAIL_IN_LOCALHOST = (
    True if os.getenv("SEND_EMAIL_IN_LOCALHOST", "false").lower() == "true" else False
)

EMAIL_ENCRYPT_KEY = os.getenv("EMAIL_ENCRYPT_KEY", " ")



# File Uploads
UPLOAD_FOLDER = "data"  # 'scrapegod/blueprints/page/pdfs'
# UPLOAD_FOLDER = 'scrapegod/blueprints/page/pdfs'
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

# Google API
CLIENT_ID = os.getenv("CLIENT_ID", None)
CLIENT_SECRET = os.getenv("CLIENT_SECRET", None)

# Somewhere in webapp_example.py, before the app.run for example
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# Google Analytics.
ANALYTICS_GOOGLE_UA = os.getenv("ANALYTICS_GOOGLE_UA", None)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.

PUBSUB_VERIFICATION_TOKEN = os.getenv("PUBSUB_VERIFICATION_TOKEN", None)
PUBSUB_TOPIC = "gmailTrigger"
GOOGLE_CLOUD_PROJECT = "blogdatabase"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


# Google credentials.json
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"

# As of 11/01/21 REDIRECT URI is only in development env so in production its .com.au domain
# FOR DEVELOPMENT 'http://localhost:8000/oauth2callback
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/oath2callback")
GOOGLE_SCOPES = """[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        ]"""
ADMIN_GOOGLE_SCOPES = """[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/user.organization.read",
        "https://www.googleapis.com/auth/user.emails.read",
        "https://www.googleapis.com/auth/profile.emails.read",
        "https://www.googleapis.com/auth/contacts",
        "https://www.googleapis.com/auth/directory.readonly"
        ]"""
# Use env file to change scopes between dev and production
# SCOPES = json.loads(os.getenv("ADMIN_GOOGLE_SCOPES", ADMIN_GOOGLE_SCOPES))
# # Raises JSON decode error in production form not reading .env file...
SCOPES = json.loads(ADMIN_GOOGLE_SCOPES)
TOKEN_URI = "https://oauth2.googleapis.com/token"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)

# in:inbox -category:{social promotions updates forums}'
METER_QUERY = "from: MyData@ausnetservices.com.au OR subject: meter data"

# Billing.
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", None)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", None)
STRIPE_API_VERSION = "2020-08-27"
STRIPE_CURRENCY = "aud"

# Go Cardless
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
PAYMENT_ENVIRONMENT = os.getenv("PAYMENT_ENVIRONMENT", "live")

# MixPanel
DEV_TOKEN = os.getenv("DEV_TOKEN", None)
# If PROD_TOKEN not found, use dev_token
PROD_TOKEN = os.getenv("PROD_TOKEN", "ced22a6592327be945015cf4cabd6b1c")

# ElasticSearch
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")
EMAIL_ENCRYPT_SECRET_PASS = os.environ.get("EMAIL_ENCRYPT_SECRET_PASS")

KINDE_CLIENT_ID = os.environ.get("KINDE_CLIENT_ID")
KINDE_CLIENT_SECRET = os.environ.get("KINDE_CLIENT_SECRET")
KINDE_DOMAIN = os.environ.get("KINDE_DOMAIN")


INVOICE_XERO_CLIENT_ID = os.environ.get("INVOICE_XERO_CLIENT_ID")
INVOICE_XERO_SECRET = os.environ.get("INVOICE_XERO_SECRET")

XERO_WEBHOOK_URL = os.environ.get("XERO_WEBHOOK_URL")

TASK_EMAIL_USERNAME = os.environ.get("TASK_EMAIL_USERNAME")
TASK_EMAIL_PASSWORD = os.environ.get("TASK_EMAIL_PASSWORD")

# Parsing
STATES = ["VIC", "NSW", "QLD", "ACT", "SA", "WA", "NT"]
BILL_COMBINE_DAYS_LIMIT = 7
BILL_COMBINE_TOTAL_LIMIT = 250

# AWS
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", None)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", None)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)

# Airwallex
AIRWALLEX_CLIENT_ID = os.getenv("AIRWALLEX_CLIENT_ID", None)
AIRWALLEX_SK = os.getenv("AIRWALLEX_SK", None)
AIRWALLEX_PK = os.getenv("AIRWALLEX_PK", None)

# Close CRM
CLOSE_API_KEY = os.getenv("CLOSE_API_KEY", None)
PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", True)
JWT_ACCESS_TOKEN_EXPIRES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", timedelta(days=30))
JWT_REFRESH_TOKEN_EXPIRES = os.getenv("JWT_REFRESH_TOKEN_EXPIRES", timedelta(days=30))
JWT_TOKEN_LOCATION = ["cookies"]
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
JWT_COOKIE_CSRF_PROTECT = False
JWT_SESSION_COOKIE = False

# FRONT API
FRONT_API_TOKEN = os.getenv("FRONT_API_TOKEN", None)

# scrapegod REACT FRONTEND
scrapegod_REACT_BASE_URL = os.getenv(
    "scrapegod_REACT_BASE_URL", "http://app.revelroad.co"
)

# MISSIVE
MISSIVE_API_TOKEN = os.getenv("MISSIVE_API_TOKEN", None)
FLASK_ENV = os.getenv("FLASK_ENV")

IGNORE_BILL_UPLOAD = (
    True if os.getenv("IGNORE_BILL_UPLOAD", "false").lower() == "true" else False
)

# App Variable
OFFER_ACTIVE_MONTH = 3

SLACK_PDS_WEBHOOK_URL = os.getenv("SLACK_PDS_WEBHOOK_URL", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")

ADMIN_TEAM_EMAILS = os.getenv(
    "ADMIN_TEAM_EMAILS",
    "bkash.timsina@gmail.com",
)
