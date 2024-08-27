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

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_db(app):
    with app.app_context():
        db.create_all()  # Ensure all tables are created before each test

        # Clear any existing data
        User.query.delete()
        Ticket.query.delete()  # Clear the Ticket table

        # Create test users only
        admin = User(username='admin', password='adminpassword', role='admin')
        regular_user = User(username='user', password='userpassword', role='regular')

        db.session.add(admin)
        db.session.add(regular_user)
        db.session.commit()

         # Create a test ticket
        ticket = Ticket(
            subject='Test Ticket',
            description='This is a test ticket.',
            status='Open',
            user_id=regular_user.id,  # Associate with the regular user
            author=regular_user.username,
            date_created=datetime.utcnow()
        )
        db.session.add(ticket)
        db.session.commit()

    yield db  # Provide the initialized database to the test

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Drop tables after each test