import pytest
from app import create_app, db
from app.models import User, Ticket
from datetime import datetime
from app.config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        # Create all tables in the database
        db.create_all()
        yield app
        # Cleanup after tests are done
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_db(app):
    # Clear any existing data and create new tables before each test
    with app.app_context():
        db.create_all()
        
        # Clear existing data
        User.query.delete()
        Ticket.query.delete()
        
        # Add new data
        admin = User(username='admin', password='adminpassword', role='admin')
        regular_user = User(username='user', password='userpassword', role='regular')
        
        db.session.add(admin)
        db.session.add(regular_user)
        db.session.commit()
        
        # Add a test ticket
        ticket = Ticket(
            subject='Test Ticket',
            description='This is a test ticket.',
            status='Open',
            user_id=regular_user.id,
            author=regular_user.username,
            date_created=datetime.utcnow()
        )
        db.session.add(ticket)
        db.session.commit()
    
    yield db