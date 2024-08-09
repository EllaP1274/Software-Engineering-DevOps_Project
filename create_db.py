from app import create_app, db

# Create an instance of the Flask app
app = create_app()

# Create tables within the application context
with app.app_context():
    db.create_all()




