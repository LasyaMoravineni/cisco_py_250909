"""
db.py - Database initialization
"""

from app.models import db
from app.config import config


def init_db(application):
    """Initialize database with Flask app"""
    application.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URL"]
    application.config["SQLALCHEMY_ECHO"] = True
    db.init_app(application)

    with application.app_context():
        db.create_all()
