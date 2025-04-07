import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address)
celery = Celery(__name__)

def make_celery(app):
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.task_track_started = True
    celery.conf.task_serializer = 'json'
    celery.conf.accept_content = ['json']
    celery.conf.result_serializer = 'json'
    celery.conf.timezone = 'UTC'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(config_name=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/taskdb")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CELERY_BROKER_URL'] = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    app.config['CELERY_RESULT_BACKEND'] = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    CORS(app)

    make_celery(app)

    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp, url_prefix="/api")

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")


    @app.route("/")
    def index():
        return {"message": "Flask Task Manager API is running"}, 200

    return app
