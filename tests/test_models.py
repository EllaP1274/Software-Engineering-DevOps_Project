import pytest
from app.models import User, Ticket
from app import db
from datetime import datetime

def test_user_repr():
    user = User(username='testuser', password='testpass', role='user')
    assert repr(user) == '<User testuser>'

def test_ticket_creation(init_db):
    user = User.query.first()  # Fetch the test user
    print(f'Fetched user: {user}')  # Debug statement

    # Create a Ticket with all fields
    ticket = Ticket(
        subject='Test Ticket',
        description='This is a test ticket.',
        status='Open',
        user_id=user.id,  # Ensure the user exists
        author=user.username,  # Author should be the username
        date_created=datetime.utcnow()
    )
    db.session.add(ticket)
    db.session.commit()

    # Verify the number of tickets
    ticket_count = Ticket.query.count()
    print(f'Number of tickets in database: {ticket_count}')  # Debug statement
    assert ticket_count == 1, f"Expected 1 ticket, but found {ticket_count}"

    # Assert the ticket is created and fields are correct
    created_ticket = Ticket.query.first()
    print(f'Created ticket: {created_ticket}')  # Debug statement
    assert created_ticket is not None  # Ensure a ticket was created
    assert created_ticket.subject == 'Test Ticket'
    assert created_ticket.description == 'This is a test ticket.'
    assert created_ticket.status == 'Open'
    assert created_ticket.user_id == user.id
    assert created_ticket.author == user.username
    assert isinstance(created_ticket.date_created, datetime)