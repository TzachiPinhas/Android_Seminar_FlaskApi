from flask import Flask
from flasgger import Swagger
from mongodb_connection_manager import MongoConnectionHolder
from routes import initial_routes
import os

app = Flask(__name__)
Swagger(app)

# חיבור למסד הנתונים
MongoConnectionHolder.initialize_db()

# רישום הנתיבים
initial_routes(app)

@app.route('/')
def home():
    return "Welcome to the Flask API! The server is running."


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', debug=True, port=port)