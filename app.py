from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils.encrypt import hash_password
from utils.checkPassword import check_password
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import uuid
from sqlalchemy import DateTime
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route("/user/get-info", methods=["GET"])
def get_user():
    username = request.json.get("username")
    response = User.query.filter_by(username=username).first()
    
    if not response:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "username": response.username,
        "id": response.id
    }), 200

@app.route('/user/register', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    
    hashed_password = hash_password(password)
    new_user = User(id=str(uuid.uuid4()),username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': 'An error occurred: ' + str(e)}), 500

@app.route("/user/auth", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "You must provide an username and a password"})
    
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/user/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route("/user/update", methods=["PUT"]) 
@jwt_required()
def update_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    new_username = data.get("username")
    new_password = data.get("password")
    
    if new_username:
        user.username = new_username
    if new_password:
        user.password = hash_password(new_password)
    
    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    createdAt = db.Column(DateTime, default=None, nullable=True)

@app.route("/task/get-info", methods=["GET"])
def get_task():
    task_id = request.json.get("id")
    response = Task.query.filter_by(id=task_id).first()
    
    if not response:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "title": response.title,
        "description": response.description,
        "createdAt": response.createdAt
    }), 200

@app.route('/task/create', methods=['POST'])
@jwt_required()
def create_task():
    username = get_jwt_identity()
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if not title or not description:
        return jsonify({'message': 'Missing title or description'}), 400
    
    new_task = Task(id=str(uuid.uuid4()),title=title, description=description, author=username,  createdAt=datetime.utcnow())
    
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': 'An error occurred: ' + str(e)}), 500

@app.route("/task/delete", methods=["DELETE"])
@jwt_required()
def delete_task():
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    
    task = Task.query.filter_by(id=data.get("id")).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    if username != task.author:
        return jsonify({"message": "You cannot delete others' task"}), 403
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route("/task/update", methods=["PUT"]) 
@jwt_required()
def update_task():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    
    task = Task.query.filter_by(id=data.get("id")).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    new_title = data.get("title")
    new_description = data.get("description")
    
    if new_title:
        task.title = new_title
    if new_description:
        task.description = new_description
    
    if task.author != username:
        return jsonify({"message": "You cannot update others' task"}), 401
    try:
        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
