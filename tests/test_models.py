import pytest
from app.models import User, Ticket
from app import db
from datetime import datetime

def test_user_repr():
    user = User(username='testuser', password='testpass', role='user')
    assert repr(user) == '<User testuser>'

def test_ticket_creation(init_db):
    user = User.query.first()  # Fetch the test user

    # Verify the number of tickets
    ticket_count = Ticket.query.count()
    assert ticket_count == 1, f"Expected 1 ticket, but found {ticket_count}"
