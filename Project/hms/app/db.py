"""
db.py - Database initialization for the HMS application.
"""

from flask_sqlalchemy import SQLAlchemy

from hms.app.config import config

db = SQLAlchemy()


def init_db(application):
    """
    Initialize the database with the given Flask application.

    Args:
        application (Flask): The Flask app instance.
    """
    if "sqlalchemy" not in application.extensions:
        application.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URL"]
        application.config["SQLALCHEMY_ECHO"] = True
        db.init_app(application)

    with application.app_context():
        db.create_all()
