from flask import Blueprint, request, jsonify
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from app.schemas.task_schema import TaskSchema
from app.utils.auth import token_required
from app import db, limiter

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

    return task_schema.jsonify(task), 201

@task_bp.route("/tasks", methods=["GET"])
@limiter.limit("10/minute")
@token_required
def get_tasks():
    tasks = TaskManager.query.all()
    return task_list_schema.jsonify(tasks), 200

@task_bp.route("/task/<int:task_id>", methods=["GET"])
@token_required
def get_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    return task_schema.jsonify(task), 200

@task_bp.route("/task/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    data = request.get_json()
    errors = task_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    task.task_name = data.get("task_name", task.task_name)
    task.is_active = data.get("is_active", task.is_active)
    db.session.commit()

    return task_schema.jsonify(task), 200

@task_bp.route("/task/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
