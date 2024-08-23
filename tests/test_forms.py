import pytest
from app.forms import RegistrationForm, LoginForm, TicketForm

def test_registration_form_valid():
    form = RegistrationForm(data=dict(
        username='testuser',
        password='testpass123',
        confirm_password='testpass123'
    ))
    assert form.validate() is True

def test_registration_form_invalid_username():
    form = RegistrationForm(data=dict(
        username='user',
        password='testpass123',
        confirm_password='testpass123'
    ))
    assert form.validate() is False
    assert 'Username must be at least 6 characters long.' in form.errors['username']

def test_ticket_form_valid():
    form = TicketForm(data=dict(
        subject='Test Subject',
        description='Test Description'
    ))
    assert form.validate() is True

def test_ticket_form_invalid_description():
    form = TicketForm(data=dict(
        subject='Subject',
        description='Short'
    ))
    assert form.validate() is False
    assert 'Field must be at least 6 characters long.' in form.errors['description']
