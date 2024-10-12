import os
import unittest
import json
from app import create_app, db, Message

class AppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()
            message1 = Message(body='Hello World!', username='Ian')
            message2 = Message(body='This is a test.', username='Alice')
            db.session.add(message1)
            db.session.add(message2)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()
        if os.path.exists('test.db'):
            os.remove('test.db')  # Remove the file if it exists

    def test_get_messages(self):
        response = self.client.get('/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)  # Expect 2 messages seeded

    def test_create_message(self):
        new_message = {
            'body': 'New Message',
            'username': 'Bob'
        }
        response = self.client.post('/messages', data=json.dumps(new_message), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Message', response.get_data(as_text=True))

    def test_update_message(self):
        with self.app.app_context():  # Ensure app context is pushed
            message = Message.query.first()
            updated_data = {
                'body': 'Updated message!'
            }
            response = self.client.patch(f'/messages/{message.id}', data=json.dumps(updated_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Updated message!', response.get_data(as_text=True))

    def test_delete_message(self):
        with self.app.app_context():  # Ensure app context is pushed
            message = Message.query.first()
            response = self.client.delete(f'/messages/{message.id}')
            self.assertEqual(response.status_code, 204)
            self.assertIsNone(Message.query.get(message.id))

if __name__ == '__main__':
    unittest.main()