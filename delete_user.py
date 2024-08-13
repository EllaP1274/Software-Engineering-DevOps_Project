from app import create_app, db
from app.models import User, Ticket
from sqlalchemy.exc import SQLAlchemyError

# Create the app and bind the database
app = create_app()
app.app_context().push()

def delete_user(user_id):
    try:
        session = db.session
        user = session.get(User, user_id)
        if user:
            # Delete associated tickets first
            tickets = Ticket.query.filter_by(user_id=user_id).all()
            for ticket in tickets:
                session.delete(ticket)
            
            # Now delete the user
            session.delete(user)
            session.commit()
            print(f'User with ID {user_id} and related tickets have been deleted.')
        else:
            print(f'User with ID {user_id} not found.')
    except SQLAlchemyError as e:
        session.rollback()
        print(f'Error occurred: {e}')

if __name__ == '__main__':
    user_id = int(input("Enter the ID of the user to delete: "))
    delete_user(user_id)


