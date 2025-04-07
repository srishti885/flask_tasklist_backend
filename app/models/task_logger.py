from app import db

class TaskLogger(db.Model):
    __tablename__ = 'task_logs'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
