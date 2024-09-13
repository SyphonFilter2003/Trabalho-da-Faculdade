from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

cred = credentials.Certificate("API/key.json")
default_app = initialize_app(cred)

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    
    jwt = JWTManager(app)
   
    from .userAPI import userAPI
    from .taskAPI import taskAPI
    
    app.register_blueprint(userAPI, url_prefix='/user')
    app.register_blueprint(taskAPI, url_prefix='/task')

    return app 
