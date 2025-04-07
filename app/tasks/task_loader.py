from app import celery, db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from datetime import date

@celery.task
def load_active_tasks():
    today = date.today()
    active_tasks = TaskManager.query.filter(TaskManager.status != 'done').all()

    created_logs = 0
    for task in active_tasks:
        existing_log = TaskLogger.query.filter_by(task_id=task.id, created_at=today).first()
        if not existing_log:
            log = TaskLogger(task_id=task.id, status="Loaded")
            db.session.add(log)
            created_logs += 1

    db.session.commit()
    return f"{created_logs} tasks loaded"
