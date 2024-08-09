from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Ticket

# Define the Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket.query.all()
    return render_template('dashboard.html', tickets=tickets)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'regular'  # Default role
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Login failed. Check your username and/or password.', 'danger')
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/promote/<int:user_id>')
@login_required
def promote_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get(user_id)
    if user:
        user.role = 'admin'
        db.session.commit()
        flash(f'{user.username} has been promoted to admin.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/create_ticket', methods=['POST'])
@login_required
def create_ticket():
    subject = request.form['subject']
    description = request.form['description']
    ticket = Ticket(subject=subject, description=description, user_id=current_user.id)
    db.session.add(ticket)
    db.session.commit()
    flash('Ticket created!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/update_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket and ticket.user_id == current_user.id:
        ticket.subject = request.form['subject']
        ticket.description = request.form['description']
        db.session.commit()
        flash('Ticket updated!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket and ticket.user_id == current_user.id:
        db.session.delete(ticket)
        db.session.commit()
        flash('Ticket deleted!', 'success')
    return redirect(url_for('main.dashboard'))



