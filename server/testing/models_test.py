import os
import unittest
from server.app import app, db, Message

class MessageModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()  # Create the test database tables

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()  # Drop the test database tables
        if os.path.exists('test.db'):
            os.remove('test.db')  # Remove the file if it exists

    def test_message_creation(self):
        with self.app.app_context():
            message = Message(body='Test message', username='TestUser')
            db.session.add(message)
            db.session.commit()
            self.assertEqual(message.body, 'Test message')
            self.assertEqual(message.username, 'TestUser')
            self.assertIsNotNone(message.id)  # Check if an ID was assigned

    def test_message_to_dict(self):
        with self.app.app_context():
            message = Message(body='Test message', username='TestUser')
            db.session.add(message)
            db.session.commit()

            expected_dict = {
                'id': message.id,
                'body': message.body,
                'username': message.username,
            }
            self.assertEqual(message.to_dict(), expected_dict)

    def test_message_update(self):
        with self.app.app_context():
            message = Message(body='Original message', username='User1')
            db.session.add(message)
            db.session.commit()

            # Update the message's body
            message.body = 'Updated message'
            db.session.commit()

            self.assertEqual(message.body, 'Updated message')

    def test_message_deletion(self):
        with self.app.app_context():
            message = Message(body='Message to delete', username='User2')
            db.session.add(message)
            db.session.commit()
            message_id = message.id  # Save the id for later verification

            db.session.delete(message)
            db.session.commit()

            # Check that the message no longer exists
            self.assertIsNone(Message.query.get(message_id))

if __name__ == '__main__':
    unittest.main()