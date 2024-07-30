import logging
from flask import Flask
from scrapegod.scrapers import scraper
from celery import Celery
from werkzeug.debug import DebuggedApplication

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """

    logging.getLogger("watchdog.observers.inotify_buffer").disabled = True

    app = Flask(__name__)

    app.config.from_object("config.settings")
    app.register_blueprint(scraper)

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


celery_app = create_celery_app()
