#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import create_app, db  # Make sure to import create_app
from models import Message  # Adjust the import according to your structure

# Create an instance of Faker
fake = Faker()

# Generate usernames
usernames = [fake.first_name() for _ in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    # Query the database to delete existing messages
    db.session.query(Message).delete()  # Delete existing messages

    messages = []

    for _ in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    # Add all new messages to the session and commit
    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():  # Ensure you're within an app context
        make_messages()
        print("Messages seeded!")  # Optional: Confirmation message
