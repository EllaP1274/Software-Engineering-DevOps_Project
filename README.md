# Software-Engineering-Agile_Project
This project is for my Software Engineering &amp; Agile assignment

To install python
python3

To create a virtual environment
python3 -m venv venv

To install Flask and other required packages
pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Login Flask-Migrate

I have used Render a hosting platform - Render does take a while to spin up and does stop after a while of inactivity so you will need to re-run the render commands. The free instance will spin down with inactivity, which can delay requests by 50 seconds or more.

You may need to run
pip install flask-admin - that creates an admin panel where you can manage users, tickets and other models directly from the web interface.

You will need to register an account first for a regular user and then the login page will pop up, you will then need to login using the same username and password you registered with. Or you can login with the admin username and password: username - admin and password - password.

The commands to set environmental variables are 
set FLASK_APP=main.py
set FLASK_ENV=development

The database is in the instance folder and is called site.db
To view the database you will need to install the SQLite viewer extension by Florian Klampfer in Visual Studio Code. Click on the site.db file and click open anyway then at the top an option should appear for SQLite Viewer, click that and you can view the database.

The command to create the database is python create_db.py

To create an admin user run
flask shell
Then run these commands in the flask shell terminal to add an admin or regular user, just change the role to regular for a regular user. Refresh the database using the refresh icon, above the tables, to view the new user in the database.
admin_user = User(username='admin', password='password', role
='admin')
db.session.add(admin_user)
db.session.commit() 

You can change a users role in the flask shell terminal using
user = User.query.filter_by(username='username_to_change').first()
user.role = 'admin'
db.session.commit()

If you delete a record just refresh the database and you will see the record is gone.

This app is an IT Helpdesk System
Students: Report technical issues with school-provided devices, such as laptops, tablets, or access to online resources.
Teachers: Submit requests for technical support in their classrooms, such as fixing projectors, or internet issues, or setting up software.
IT Staff: Use the system to track, manage, and resolve reported issues. They can update, and mark tickets as resolved.

Tickets are ordered by status, so open ones appear at the top of all tickets and closed tickets are aat the bottom. 
Tickets are also ordered based on date and time of creation. New, open tickets are nearer the top of all tickets so if a ticket is urgent it can be handeled ASAP.

The command to build the app is
pip install -r requirements.txt

To start the render deployment run 
waitress-serve --host=127.0.0.1 --port=5000 main:app

The command to run the web app is 
python main.py

You can run python delete_user.py to delete any unwanted users.
