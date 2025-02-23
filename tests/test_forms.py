import pytest
from app.forms import RegistrationForm, LoginForm, TicketForm
from app import create_app, db
from app.models import User
from app.config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_registration_form_valid():
    """Test valid registration form."""
    form = RegistrationForm(data=dict(
        username='validuser1',
        password='validpass12',
        confirm_password='validpass12'
    ))
    assert form.validate() is True

def test_registration_form_invalid_username_too_short():
    """Test username that is too short."""
    form = RegistrationForm(data=dict(
        username='short',  # Username is less than 6 characters
        password='validpass1',
        confirm_password='validpass1'
    ))
    assert form.validate() is False  # The form should not validate successfully
    assert 'Username must be at least 6 characters long.' in form.errors['username']

def test_registration_form_invalid_username_too_many_numbers():
    """Test username with too many numbers."""
    form = RegistrationForm(data=dict(
        username='user1234',
        password='validpass12',
        confirm_password='validpass12'
    ))
    assert form.validate() is False
    assert 'Username must contain no more than 3 numbers.' in form.errors['username']

def test_registration_form_invalid_password_too_short():
    """Test password that is too short."""
    form = RegistrationForm(data=dict(
        username='validuser1',
        password='short1',
        confirm_password='short1'
    ))
    assert form.validate() is False
    assert 'Password must be at least 6 characters long' in form.errors['password'] or \
           'Password must include at least 2 numbers' in form.errors['password']

def test_registration_form_invalid_password_too_few_numbers():
    """Test password with too few numbers."""
    form = RegistrationForm(data=dict(
        username='validuser1',
        password='password',
        confirm_password='password'
    ))
    assert form.validate() is False
    assert 'Password must include at least 2 numbers' in form.errors['password']

def test_registration_form_valid_password():
    """Test valid password."""
    form = RegistrationForm(data=dict(
        username='validuser1',
        password='validpass12',
        confirm_password='validpass12'
    ))
    assert form.validate() is True

def test_login_form_valid():
    """Test valid login form."""
    form = LoginForm(data=dict(
        username='validuser1',
        password='validpass123'
    ))
    assert form.validate() is True

def test_login_form_invalid_username_too_short():
    """Test username that is too short."""
    form = LoginForm(data=dict(
        username='user1',
        password='validpass123'
    ))
    assert form.validate() is False
    assert 'Username must be at least 6 characters long.' in form.errors['username']

def test_login_form_invalid_username_too_many_numbers():
    """Test username that has more than 3 numbers."""
    form = LoginForm(data=dict(
        username='user1234',
        password='validpass123'
    ))
    assert form.validate() is False
    assert 'Username must contain no more than 3 numbers.' in form.errors['username']

def test_login_invalid_password(init_db, client):
    """Test login with invalid password."""
    with client.application.app_context():  # Explicitly push the app context
        user = User(username='testuser', password='correctpassword', role='regular')
        db.session.add(user)
        db.session.commit()

    # Try logging in with an incorrect password
    response = client.post('/login', data=dict(
        username='testuser',
        password='wrongpassword'
    ))

    # Check for the login failure message
    assert response.status_code == 200
    assert b'Login failed. Check your username and/or password.' in response.data

def test_ticket_form_valid():
    """Test valid ticket form."""
    form = TicketForm(data=dict(
        subject='Valid Subject',
        description='Valid description with more than 6 characters'
    ))
    assert form.validate() is True

def test_ticket_form_invalid_subject_too_short():
    """Test subject that is too short."""
    form = TicketForm(data=dict(
        subject='Short',
        description='Valid description'
    ))
    assert form.validate() is False
    assert 'Field must be between 6 and 150 characters long.' in form.errors['subject']

def test_ticket_form_invalid_description_too_short():
    """Test description that is too short."""
    form = TicketForm(data=dict(
        subject='Valid Subject',
        description='Short'
    ))
    assert form.validate() is False
    assert 'Field must be at least 6 characters long.' in form.errors['description']

def test_ticket_form_invalid_subject_too_many_numbers():
    """Test subject with too many numbers."""
    form = TicketForm(data=dict(
        subject='Subject1234',
        description='Valid description'
    ))
    assert form.validate() is False
    assert 'Field must contain no more than 3 numbers.' in form.errors['subject']

def test_ticket_form_invalid_description_too_many_numbers():
    """Test description with too many numbers."""
    form = TicketForm(data=dict(
        subject='Valid Subject',
        description='Description1234'
    ))
    assert form.validate() is False
    assert 'Field must contain no more than 3 numbers.' in form.errors['description']


