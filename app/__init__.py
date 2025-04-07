from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")

def create_app():
    app = Flask(__name__)

 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/taskdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

  
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    CORS(app)

   
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    
    @app.route("/")
    def index():
        return {"message": "Flask app is running"}, 200

    return app
