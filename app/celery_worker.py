from celery import Celery
from app import create_app, db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from datetime import date

flask_app = create_app()
celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

@celery.task
def daily_task_loader():
    with flask_app.app_context():
        today = date.today()
        active_tasks = TaskManager.query.filter_by(is_active=True).all()

        created = 0
        for task in active_tasks:
            exists = TaskLogger.query.filter_by(task_id=task.id, created_at=today).first()
            if not exists:
                log = TaskLogger(task_id=task.id, status="Loaded")
                db.session.add(log)
                created += 1

        db.session.commit()
        return f"{created} task(s) logged today."
