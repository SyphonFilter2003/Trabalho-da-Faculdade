from flask import Blueprint, request, jsonify
from firebase_admin import firestore, auth
import uuid
from flask_jwt_extended import create_access_token
import datetime
import bcrypt

db = firestore.client()
userRef = db.collection('users')

userAPI = Blueprint('userAPI', __name__)

def get_user_as_dict(user_id):
    try:
        user_doc = userRef.document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return user_data
        else:
            return jsonify({"error": "🔍 User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_by_username(username):
    try:
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).limit(1).stream()
        for user_doc in query:
            user_data = user_doc.to_dict()
            uid = user_doc.id
            return {'uid': uid, **user_data}
        return None
    except Exception as e:
        print(f"Error fetching user by username: {e}")
        return None
    
@userAPI.route("/register", methods=["POST"])
def create():
    try:
        data = request.json
        user_id = str(uuid.uuid4())
        
        if 'password' in data:
            from utils.encrypt import hash_password
            
            data['password'] = hash_password(data['password']).decode('utf-8')
        
        userRef.document(user_id).set(data)
        return jsonify({"message": "🎈 User created successfully. Congrats! 🌟"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@userAPI.route("/get-user-by-id/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user_doc = userRef.document(user_id).get()
        if user_doc.exists:
            return jsonify(user_doc.to_dict()), 200
        else:
            return jsonify({"error": "🔍 User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@userAPI.route("/delete-user-by-id/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user_doc_ref = userRef.document(user_id)
        if user_doc_ref.get().exists:
            user_doc_ref.delete()
            return jsonify({"message": "😿 User deleted successfully."}), 200
        else:
            return jsonify({"error": "🔍 User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@userAPI.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username and password:
        try:
            user = get_user_by_username(username)
            if user:
                stored_password_hash = user.get('password')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    expiration_time = datetime.timedelta(hours=1)
                    access_token = create_access_token(identity=user['uid'], expires_delta=expiration_time)
                    return jsonify(access_token=access_token), 200
                else:
                    return jsonify({"error": "Incorrect password."}), 401
            else:
                return jsonify({"error": "User not found."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "📃 You must provide all credentials."}), 400