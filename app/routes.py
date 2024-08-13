from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Ticket
from app.forms import RegistrationForm, LoginForm

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
    # Check if the current user is an admin
    if current_user.role == 'admin':
        # Fetch all tickets for admins
        tickets = Ticket.query.all()
    else:
        # Fetch only the tickets created by the current user
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()

    # Sort tickets: open tickets first, then closed tickets
    tickets.sort(key=lambda t: (t.status == 'closed', t.id))

    return render_template('dashboard.html', tickets=tickets)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = 'regular'  # Default role
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html', form=form)

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
    if ticket:
        if current_user.role == 'admin' or ticket.user_id == current_user.id:
            ticket.subject = request.form['subject']
            ticket.description = request.form['description']
            db.session.commit()
            flash('Ticket updated!', 'success')
        else:
            flash('Access denied. You can only edit your own tickets.', 'danger')
    else:
        flash('Ticket not found.', 'danger')
    return redirect(url_for('main.dashboard'))

@main.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        new_status = request.form.get('status')
        if new_status in ['open', 'closed']:
            ticket.status = new_status
            db.session.commit()
            flash('Ticket status updated successfully.', 'success')
        else:
            flash('Invalid status.', 'danger')
    else:
        flash('Ticket not found.', 'danger')
    
    return redirect(url_for('main.dashboard'))

@main.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        if current_user.role == 'admin':
            db.session.delete(ticket)
            db.session.commit()
            flash('Ticket deleted!', 'success')
        else:
            flash('Access denied. Only admins can delete tickets.', 'danger')
    else:
        flash('Ticket not found.', 'danger')
    return redirect(url_for('main.dashboard'))


