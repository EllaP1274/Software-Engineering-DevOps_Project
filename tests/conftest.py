import pytest
from app import create_app, db
from app.models import User, Ticket
from datetime import datetime
from app.config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()  # Create tables
        yield app
        db.session.remove()
        db.drop_all()  # Drop tables after tests

@pytest.fixture(scope='function')
def init_db(app):
    with app.app_context():
        db.create_all()  # Create tables for each test
        User.query.delete()
        Ticket.query.delete()

        # Add initial data if needed
        admin = User(username='admin', password='adminpassword', role='admin')
        regular_user = User(username='user', password='userpassword', role='regular')
        db.session.add(admin)
        db.session.add(regular_user)
        db.session.commit()

    yield db  # Provide the database for the test

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Clean up after the test