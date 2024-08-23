from app import create_app, db

app = create_app()

with app.app_context():
    # Check if the app is registered with SQLAlchemy
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error: {e}")
