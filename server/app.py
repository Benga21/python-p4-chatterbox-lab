from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # Import Migrate

# Initialize the database and migration
db = SQLAlchemy()
migrate = Migrate()

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username
        }

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure your database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize migrate with app and db

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    # Home route
    @app.route('/')
    def home():
        return "Welcome to the Chatterbox API! Use /messages to interact with messages."

    # GET route to retrieve all messages
    @app.route('/messages', methods=['GET'])
    def get_messages():
        messages = Message.query.order_by(Message.id.asc()).all()
        return jsonify([message.to_dict() for message in messages]), 200

    # POST route to create a new message
    @app.route('/messages', methods=['POST'])
    def create_message():
        data = request.get_json()

        if not data or not data.get('body') or not data.get('username'):
            return jsonify({"error": "Both 'body' and 'username' fields are required."}), 400

        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

    # PATCH route to update an existing message
    @app.route('/messages/<int:id>', methods=['PATCH'])
    def update_message(id):
        message = Message.query.get_or_404(id)
        data = request.get_json()

        if not data or not data.get('body'):
            return jsonify({"error": "'body' field is required."}), 400

        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200

    # DELETE route to delete a message
    @app.route('/messages/<int:id>', methods=['DELETE'])
    def delete_message(id):
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"}), 204

    return app

# Create an app instance for running purposes
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
