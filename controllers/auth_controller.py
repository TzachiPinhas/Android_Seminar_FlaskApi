from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from mongodb_connection_manager import MongoConnectionHolder
from flask_bcrypt import Bcrypt
from bson import ObjectId

import os

# יצירת Blueprint לאימות משתמשים
auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()
db = MongoConnectionHolder.get_db()

# מפתח סודי ליצירת JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

# 📥 הרשמה
@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Username for the new user
            password:
              type: string
              description: Password for the new user
    responses:
      201:
        description: User registered successfully
      400:
        description: Username already exists or missing fields
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if db['users'].find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    # יצירת מזהה ייחודי ואבטחת סיסמה
    user_id = str(ObjectId())
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    db['users'].insert_one({
        "_id": user_id,
        "username": username,
        "password_hash": hashed_password,
        "role": "user"
    })

    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201

# 🔑 התחברות
@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Username for login
            password:
              type: string
              description: Password for login
    responses:
      200:
        description: Login successful, returns user ID
      401:
        description: Invalid username or password
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db['users'].find_one({"username": username})

    if not user or not bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful!", "user_id": str(user["_id"])}), 200
