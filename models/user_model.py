from pymongo import MongoClient

class UserModel:
    def __init__(self, db):
        self.collection = db['users']

    def create_user(self, username, hashed_password, role="user"):
        user = {
            "username": username,
            "password": hashed_password,
            "role": role
        }
        self.collection.insert_one(user)

    def find_by_username(self, username):
        return self.collection.find_one({"username": username})
