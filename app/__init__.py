from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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

        # Define the AdminModelView class to restrict admin access
        class AdminModelView(ModelView):
            def is_accessible(self):
                return current_user.is_authenticated and current_user.role == 'admin'

        # Set up Flask-Admin
        admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

        # Add views to the admin panel with the custom AdminModelView
        admin.add_view(AdminModelView(User, db.session))
        admin.add_view(AdminModelView(Ticket, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

