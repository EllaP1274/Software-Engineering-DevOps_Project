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

The commands to set environmental variables are 
set FLASK_APP=main.py
set FLASK_ENV=development

The command to create the database is python create_db.py
The database is in the instance folder and is called site.db
To view the database you will need to install the SQLite extension by alexcvzz in Visual Studio Code.

The command to run the web app is 
python main.py

You will need to register an account first and then the login page will pop up you will then need to login using the same username and password you registered with.