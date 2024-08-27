import pytest
from app import db
from flask_login import login_user
from app.models import User, Ticket
from datetime import datetime
from sqlalchemy import inspect

@pytest.fixture
def logged_in_client(client, init_db):
    client.post('/login', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    return client

def test_dashboard_logged_in(logged_in_client):
    # Ensure user is logged in before accessing the dashboard
    response = logged_in_client.get('/dashboard')
    
    # Check that the status code is 200 (OK) and that the content is as expected
    assert response.status_code == 200

    # Check for specific content on the dashboard
    assert b'Dashboard' in response.data  # Replace 'Dashboard' with actual expected content

    # Optionally, check for the presence of the form and tickets if applicable
    assert b'Create Ticket' in response.data  # Example: Check if the create ticket form is present

def test_register(client):
    response = client.post('/register', data=dict(
        username='newuser',
        password='newpassword'
    ), follow_redirects=True)  # Follow redirects to the final page

    assert response.status_code == 200

def test_login(client):
    response = client.post('/login', data=dict(username='admin', password='adminpassword'), follow_redirects=True)
    assert response.status_code == 200  # Should be 200 after following the redirect

def test_ticket_table_created(app):
    with app.app_context():
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        assert 'ticket' in table_names

def test_create_ticket(logged_in_client, init_db):
    """Test ticket creation."""
    response = logged_in_client.post('/create_ticket', data={
        'subject': 'New Ticket',
        'description': 'This is a new ticket'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Ticket created successfully!' in response.data

def test_update_ticket(logged_in_client, init_db):
    user = User.query.filter_by(username='user').first()
    ticket = Ticket(
        subject='Old Subject',
        description='Old Description',
        user_id=user.id,
        status="Open",
        author=user.username,
        date_created=datetime.utcnow()
    )
    db.session.add(ticket)
    db.session.commit()

    response = logged_in_client.post(f'/update_ticket/{ticket.id}', data=dict(
        subject='New Subject',
        description='New Description',
        status="Open"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Ticket updated successfully!' in response.data

def test_delete_ticket(logged_in_client, init_db):
    # Ensure there is a ticket to delete
    ticket = Ticket.query.first()
    assert ticket is not None, "No ticket found in database"

    # Send POST request to delete the ticket
    response = logged_in_client.post(f'/delete_ticket/{ticket.id}', follow_redirects=True)

    # Verify the response
    assert response.status_code == 200

    # Verify the flash message
    assert b'Ticket deleted successfully!' in response.data, "Flash message not found in response"

    # Verify the ticket was deleted
    deleted_ticket = Ticket.query.get(ticket.id)
    assert deleted_ticket is None, "Ticket should have been deleted"

def test_logout(logged_in_client, init_db):
    user = User.query.filter_by(username='user').first()
    assert user is not None
    
    with logged_in_client:
        # Login the user
        logged_in_client.post('/login', data=dict(username='user', password='userpassword'), follow_redirects=True)
        
        # Now logout
        response = logged_in_client.post('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Login' in response.data