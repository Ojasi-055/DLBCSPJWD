# This file sets up the SQLAlchemy database instance for the Flask application.
# Approach: Separate the database configuration and initialization into its own module for better organization.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()