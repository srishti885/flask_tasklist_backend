from flask import Blueprint, request, jsonify
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from app.schemas.task_schema import TaskSchema
from app.utils.auth import token_required
from app import db, limiter
from datetime import datetime, date
import csv
import io

task_bp = Blueprint('task', __name__)
task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

@task_bp.route("/task", methods=["POST"])
@token_required
def create_task():
    data = request.get_json()
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    task = TaskManager(**data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201

@task_bp.route("/tasks", methods=["GET"])
@limiter.limit("10/minute")
@token_required
def get_tasks():
    date_param = request.args.get("date")
    if date_param:
        try:
            date_obj = datetime.strptime(date_param, "%Y-%m-%d").date()
            tasks = TaskManager.query.filter(db.func.date(TaskManager.created_at) == date_obj).all()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    else:
        tasks = TaskManager.query.all()

    return jsonify(task_list_schema.dump(tasks)), 200

@task_bp.route("/task/<int:task_id>", methods=["GET"])
@token_required
def get_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    return jsonify(task_schema.dump(task)), 200

@task_bp.route("/task/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    data = request.get_json()
    errors = task_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(task_schema.dump(task)), 200

@task_bp.route("/task/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

@task_bp.route("/upload-csv", methods=["POST"])
@token_required
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)

    created = 0
    for row in csv_input:
        if 'title' in row and 'description' in row and 'status' in row:
            task = TaskManager(title=row['title'], description=row['description'], status=row['status'])
            db.session.add(task)
            created += 1
    db.session.commit()

    return jsonify({'message': f'{created} tasks created from CSV.'}), 201

@task_bp.route("/debug-loader", methods=["GET"])
def debug_loader():
    try:
        active_tasks = TaskManager.query.filter(TaskManager.status != 'done').all()
        today = date.today()
        created_logs = 0

        for task in active_tasks:
            existing_log = TaskLogger.query.filter_by(task_id=task.id, created_at=today).first()
            if not existing_log:
                log = TaskLogger(task_id=task.id, status="Loaded")
                db.session.add(log)
                created_logs += 1

        db.session.commit()
        return jsonify({"message": f"{created_logs} task logs created today."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
