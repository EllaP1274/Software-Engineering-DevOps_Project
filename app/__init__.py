from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app context
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Import and register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)

    # Import models here to avoid circular import issues
    with app.app_context():
        from app.models import User, Ticket

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
