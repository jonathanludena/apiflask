from flask import request, jsonify, Blueprint
from datetime import datetime

from database import tasks

task_bp = Blueprint('routes-tasks', __name__)


@task_bp.route('/tasks')
def get_tasks():
    data = tasks.select_all_tasks()

    if data:
        return jsonify({"tasks": data})
    elif data == False:
        return jsonify({"message": "Internal Error"})
    else:
        return jsonify({"tasks": {}})


@task_bp.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    created_date = datetime.now().strftime("%x")  # Format M/DD/YYYY

    data = (title, created_date)
    task_id = tasks.insert_task(data)

    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({"task": task})

    return jsonify({"message": "Internal Error"})


@task_bp.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title']
    id_arg = request.args.get('id')

    # En el tuple se debe colocar la coma para que no produzca error
    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)

    return jsonify({"message": "Internal Error"})


@task_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({"message": "Task deleted"})

    return jsonify({"message": "Internal Error"})


@task_bp.route('/tasks/completed', methods={'PUT'})
def completed_task():
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.completed_task(id_arg, completed):
        return jsonify({"message": "succesfully"})

    return jsonify({"message": "Internal Error"})
