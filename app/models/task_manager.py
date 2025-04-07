from app import db

class TaskManager(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
