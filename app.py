from flask import Flask
from flasgger import Swagger
from mongodb_connection_manager import MongoConnectionHolder
from routes import initial_routes
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

Swagger(app)
MongoConnectionHolder.initialize_db()
initial_routes(app)

@app.route('/')
def home():
    return "Welcome to the Flask API! The server is running with CORS."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', debug=True, port=port)
