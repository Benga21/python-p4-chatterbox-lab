from  server.app import create_app, db  # Import your app and db
from  server.models import Message  # Ensure you import your Message model

if __name__ == '__main__':
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():  # Use the app context
        db.create_all()  # Create all tables defined in the models
        print("Database initialized and tables created!")
