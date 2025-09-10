# This script initializes the database for the BookBank application.
# It should be run once to create the necessary tables.
# Approach: This structural separation ensures that the database setup is distinct from the application logic.

# Import the app and db instances from app.py
from app import app, db


with app.app_context():
    db.create_all()  # Create database tables for our data models

# Run the app
if __name__ == '__main__':
    app.run(debug=True)