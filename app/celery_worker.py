from celery import Celery
from app import create_app, db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger


flask_app = create_app()


celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

@celery.task
def daily_task_loader():
    with flask_app.app_context():
        active_tasks = TaskManager.query.filter_by(is_active=True).all()
        for task in active_tasks:
            # Avoid duplicate logs for same task
            existing_log = TaskLogger.query.filter_by(task_id=task.id).first()
            if not existing_log:
                log = TaskLogger(task_id=task.id, status="Loaded")
                db.session.add(log)
        
        db.session.commit()
