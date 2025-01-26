# Setup Instructions

Follow these steps to set up and run the API service:

## Prerequisites

- Python 3.8 or higher
- Flask
- MongoDB (MongoDB Atlas recommended)
- A `.env` file with database connection details

## Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/TzachiPinhas/Android_Seminar_FlaskApi.git
   cd Android_Seminar_FlaskApi
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file:

   ```makefile
   PORT= The port on which the Flask application runs.
   DB_USERNAME= Your MongoDB database username.
   DB_PASSWORD= Your MongoDB database password.
   DB_CONNECTION_STRING= The MongoDB Atlas connection string.
   DB_NAME= The name of the MongoDB database used for the application.
   SECRET_KEY= A secret key used for password hashing and securing user authentication.
   ```

4. Run the server:

   ```bash
   python app.py
   ```

The API will be available at: [https://android-seminar-flask-api.vercel.app/](https://android-seminar-flask-api.vercel.app/)

## Database

The API service is connected to a MongoDB Atlas database, which securely stores book and user data. MongoDB Atlas is a fully managed cloud database solution that ensures high availability, scalability, and security.

Ensure that your `.env` file contains valid credentials for accessing the database.

## Cross-Origin Resource Sharing (CORS)

To allow cross-origin requests, the following CORS configuration is applied in the Flask app:

```python
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})
```
# Deployment

The API service is deployed using **Vercel**, providing a scalable and easy-to-manage cloud environment.

## Deployment URL

You can access the deployed API at the following URL:

[https://android-seminar-flask-api.vercel.app/](https://android-seminar-flask-api.vercel.app/)

## Deployment Steps

1. Ensure your repository is hosted on GitHub.
2. Link the repository to your Vercel account.
3. Configure environment variables on Vercel (DB credentials, secret keys, etc.).
4. Deploy the project by clicking "Deploy" in the Vercel dashboard.
5. Monitor the deployment via Vercel's dashboard and logs.

By publishing the deployment URL, developers can quickly test the API endpoints and integrate them into their applications. The provided URL allows for easy verification and demonstration of API functionalities.





