import pytest
from flask import url_for
from app import create_app, db
from app.models import User, Ticket

@pytest.mark.parametrize('route', [
    '/',
    '/dashboard',
    '/create_ticket',
    '/login',
    '/register',
])
def test_routes(test_client, init_database, route):
    """Test that routes return the correct status code and handle redirections."""
    # Make sure the user is authenticated if the route requires it
    if route in ['/dashboard', '/create_ticket']:
        test_client.post('/login', data={
            'username': 'user',
            'password': 'password'
        }, follow_redirects=True)
    
    response = test_client.get(route, follow_redirects=True)
    
    if route in ['/login', '/register'] and not test_client.get('/').data:
        # Expect redirection for routes requiring login if the user is not authenticated
        assert response.status_code == 302
    else:
        assert response.status_code == 200

def test_register_user(test_client):
    """Test user registration."""
    response = test_client.post('/register', data={
        'username': 'newuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert User.query.filter_by(username='newuser').first() is not None

def test_login_user(test_client, init_database):
    """Test user login."""
    response = test_client.post('/login', data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    
    # Check for successful redirection and a welcome message
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_create_ticket(test_client, init_database):
    """Test ticket creation."""
    response = test_client.post('/create_ticket', data={
        'subject': 'New Ticket',
        'description': 'This is a new ticket'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify the ticket creation
    created_ticket = Ticket.query.filter_by(subject='New Ticket').first()
    assert created_ticket is not None
    assert created_ticket.description == 'This is a new ticket'

def test_update_ticket(test_client, init_database):
    """Test updating a ticket."""
    ticket = Ticket.query.first()
    response = test_client.post(f'/update_ticket/{ticket.id}', data={
        'subject': 'Updated Ticket',
        'description': 'This is an updated ticket'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    updated_ticket = Ticket.query.get(ticket.id)
    assert updated_ticket.subject == 'Updated Ticket'
    assert updated_ticket.description == 'This is an updated ticket'

def test_update_ticket_status(test_client, init_database):
    """Test updating a ticket status."""
    ticket = Ticket.query.first()
    response = test_client.post(f'/update_ticket_status/{ticket.id}', data={
        'status': 'closed'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    updated_ticket = Ticket.query.get(ticket.id)
    assert updated_ticket.status == 'closed'

def test_delete_ticket(test_client, init_database):
    """Test deleting a ticket."""
    ticket = Ticket.query.first()
    response = test_client.post(f'/delete_ticket/{ticket.id}', follow_redirects=True)
    
    assert response.status_code == 200
    
    deleted_ticket = Ticket.query.get(ticket.id)
    assert deleted_ticket is None