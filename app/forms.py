from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError
import re

def validate_username(form, field):
    # Allow "admin" to bypass validation
    if field.data == 'admin':
        return

    # Check if the username length is less than 6 characters
    if len(field.data) < 6:
        raise ValidationError('Username must be at least 6 characters long.')
    
    # Check if the username contains more than 3 numbers
    if len(re.findall(r'\d', field.data)) > 3:
        raise ValidationError('Username must contain no more than 3 numbers.')

def validate_ticket_field(form, field):
    if len(re.findall(r'\d', field.data)) > 3:
        raise ValidationError('Field must contain no more than 3 numbers.')

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), validate_username])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long'),
        Regexp(r'(?=.*\d.*\d)', message='Password must include at least 2 numbers')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), validate_username])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TicketForm(Form):
    subject = StringField('Subject', validators=[DataRequired(), validate_ticket_field, Length(min=6, max=150)])
    description = TextAreaField('Description', validators=[DataRequired(), validate_ticket_field, Length(min=6)])
    submit = SubmitField('Submit')
