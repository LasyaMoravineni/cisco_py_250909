import pytest
from hms.app import routes
from hms.app.db import db, init_db
from hms.app.routes import application

pytestmark = pytest.mark.asyncio
@pytest.fixture
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
    
@pytest.fixture
def client():
    # configure app for testing
    application.config['TESTING'] = True
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    init_db(application)

    with routes.application.app_context():
        db.create_all()
        yield routes.application.test_client()
        db.session.remove()
        db.drop_all()
