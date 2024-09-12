from flask import Blueprint, request, jsonify
from firebase_admin import firestore, auth
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime
from flask import json

db = firestore.client()
taskRef = db.collection('tasks')

taskAPI = Blueprint('taskAPI', __name__)
logging.basicConfig(level=logging.DEBUG)

@taskAPI.route("/create", methods=["POST"])
@jwt_required()
def create():
    try:
        user_id = get_jwt_identity()

        from .userAPI import get_user_as_dict
        try:
            user_data = get_user_as_dict(user_id)
        except Exception as e:
            return jsonify({"error": f"Error fetching user data: {str(e)}"}), 500

        task_id = str(uuid.uuid4())

        try:
            task_data = request.json
            task_data["author_id"] = user_id
            task_data["author_name"] = user_data.get('username')
            task_data["createdAt"] = int(datetime.now().timestamp() * 1000)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Error processing JSON data: {str(e)}"}), 400

        try:
            db.collection('tasks').document(task_id).set(task_data)
        except Exception as e:
            return jsonify({"error": f"Error inserting task into database: {str(e)}"}), 500

        return jsonify({"message": f"Task created successfully by {user_data.get('username')}"}), 201
    except Exception as e:
        return jsonify({"error": f"Error creating task: {str(e)}"}), 500
    
@taskAPI.route("/get-task-by-id/<task_id>", methods=["GET"])
def get_user(task_id):
    try:
        task_doc = taskAPI.document(task_id).get()
        if task_doc.exists:
            return jsonify(task_doc.to_dict()), 200
        else:
            return jsonify({"error": "🔍 Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@taskAPI.route("/delete-user-by-id/<task_id>", methods=["DELETE"])
def delete_user(task_id):
    try:
        task_doc_ref = taskAPI.document(task_id)
        if task_doc_ref.get().exists:
            task_doc_ref.delete()
            return jsonify({"message": "😿 Task deleted successfully."}), 200
        else:
            return jsonify({"error": "🔍 User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500