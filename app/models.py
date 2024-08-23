from app import db  # Import db from the app package
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin' or 'regular'

    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.Column(db.String(150), nullable=False)  # New column for author
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

    def __init__(self, subject, description, status, user_id, author, date_created):
        self.subject = subject
        self.description = description
        self.status = status
        self.user_id = user_id
        self.author = author
        self.date_created = date_created

    def __repr__(self):
        return f'<Ticket {self.subject}>'