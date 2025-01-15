from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# טוען את משתני הסביבה מהקובץ .env
load_dotenv()

# משתני סביבה לחיבור למסד הנתונים
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")

# יצירת מחרוזת חיבור (Connection String) עם גרסת API
MONGO_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CONNECTION_STRING}/{DB_NAME}"


class MongoConnectionHolder:
    """
    מחלקה שמנהלת חיבור יחיד (Singleton) למסד הנתונים MongoDB
    """
    __db = None

    @staticmethod
    def initialize_db():
        """
        אתחול חיבור למסד הנתונים.
        מוודא שהחיבור נפתח פעם אחת בלבד.
        """
        if MongoConnectionHolder.__db is None:
            try:
                # יצירת לקוח (Client) עם גרסת API ובדיקת חיבור
                client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

                # בדיקת חיבור (Ping) למסד הנתונים
                client.admin.command('ping')
                print("Connected to MongoDB!")

                # שמירת החיבור למחלקה
                MongoConnectionHolder.__db = client[DB_NAME]

            except Exception as e:
                # טיפול בשגיאות - מדפיס את השגיאה
                print(f"Failed to connect to MongoDB: {e}")

    @staticmethod
    def get_db():
        """
        מחזיר את חיבור מסד הנתונים.
        אם אין חיבור, מפעיל אתחול.

        :return: אובייקט של מסד הנתונים
        """
        if MongoConnectionHolder.__db is None:
            MongoConnectionHolder.initialize_db()
        return MongoConnectionHolder.__db
