import pytest
from app import db
from flask_login import login_user
from app.models import User, Ticket
from datetime import datetime

@pytest.fixture
def logged_in_client(client, init_db):
    client.post('/login', data=dict(username='admin', password='password'))
    return client

def test_dashboard_logged_in(logged_in_client):
    response = logged_in_client.get('/dashboard')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/register', data=dict(
        username='newuser',
        password='newpassword'
    ))
    assert b'Registration successful!' in response.data

def test_login(client):
    response = client.post('/login', data=dict(username='admin', password='password'))
    assert response.status_code == 302  # Redirect after login

    # Check if login was successful
    response = client.get('/dashboard')
    assert 'Welcome, testuser' in response.get_data(as_text=True)

def test_create_ticket(logged_in_client):
    response = logged_in_client.post('/create_ticket', data=dict(
        subject='New Ticket',
        description='Description of the new ticket',
        status='Open'
    ))
    assert response.status_code == 302  # Assuming redirection

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
    admin = User.query.filter_by(username='admin').first()
    login_user(admin)

    ticket = Ticket(
        subject='Ticket to Delete',
        description='Description',
        status='Open',
        user_id=admin.id,
        author=admin.username,
        date_created=datetime.utcnow()
    )
    db.session.add(ticket)
    db.session.commit()

    response = logged_in_client.post(f'/delete_ticket/{ticket.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Ticket deleted successfully!' in response.data

def test_promote_user(logged_in_client, init_db):
    admin = User.query.filter_by(username='admin').first()
    assert admin is not None

    regular_user = User.query.filter_by(username='user').first()
    assert regular_user is not None

    response = logged_in_client.get(f'/promote/{regular_user.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'promoted to admin' in response.data
    assert User.query.filter_by(username='user', role='admin').first() is not None

def test_logout(logged_in_client, init_db):
    user = User.query.filter_by(username='user').first()
    assert user is not None
    login_user(user)
    response = logged_in_client.post('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data