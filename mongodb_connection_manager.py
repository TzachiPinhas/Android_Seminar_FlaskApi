from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")

MONGO_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CONNECTION_STRING}/{DB_NAME}"


class MongoConnectionHolder:
    """
    """
    __db = None

    @staticmethod
    def initialize_db():
        """

        """
        if MongoConnectionHolder.__db is None:
            try:
                client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

                client.admin.command('ping')
                print("Connected to MongoDB!")

                MongoConnectionHolder.__db = client[DB_NAME]

            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")

    @staticmethod
    def get_db():
        """

        """
        if MongoConnectionHolder.__db is None:
            MongoConnectionHolder.initialize_db()
        return MongoConnectionHolder.__db
