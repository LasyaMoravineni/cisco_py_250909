"""
db.py - Database initialization
"""

from hms.app.config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(application):
    
    """Initialize database with Flask app"""
    if "sqlalchemy" not in application.extensions:
        application.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URL"]
        application.config["SQLALCHEMY_ECHO"] = True
        db.init_app(application)

    with application.app_context():
        db.create_all()
