import logging
from flask import Flask
from scrapegod.scrapers import scraper
from scrapegod.blueprints.user import user
from celery import Celery
from werkzeug.debug import DebuggedApplication
from flask_cors import CORS
from scrapegod.extensions import (
    cache,
    cors,
    csrf,
    db,
    ext,
    flask_static_digest,
    jwt,
    login_manager,
    argon2,
    # api,
    mail,
    flask_restful_api,
)


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """

    logging.getLogger("watchdog.observers.inotify_buffer").disabled = True

    app = Flask(__name__)

    app.config.from_object("config.settings")
    app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
    extensions(app)
    app.register_blueprint(scraper)
    app.register_blueprint(user)
    if settings_override:
        app.config.update(settings_override)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()
    # app.app_context().push()
    celery = Celery(app.import_name)  # , broker=app.config['REDIS_URL']),
    # include=CELERY_TASK_LIST)
    celery.conf.update(
        app.config.get("CELERY_CONFIG", {}),
        CELERY_TASK_SOFT_TIME_LIMIT=900,
        CELERY_TASK_TIME_LIMIT=900,
        CELERY_TASK_ACKS_LATE=True,
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # debug_toolbar.init_app(app)

    cache.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    argon2.init_app(app)
    # api.init_app(app)
    flask_restful_api.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    ext.init_app(app=app)
    flask_static_digest.init_app(app)
    db.init_app(app)

    return None


celery_app = create_celery_app()
