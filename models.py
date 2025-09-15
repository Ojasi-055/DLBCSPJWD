from db import db
from datetime import datetime, timezone

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # Unique identifier for each user
    username = db.Column(db.String(80), unique=True, nullable=False)    # Username of the user
    password = db.Column(db.String(120), nullable=False)                # Hashed password of the user
    

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # Unique identifier for each book
    title = db.Column(db.String(200), nullable=False)       # Title of the book
    author = db.Column(db.String(100), nullable=False)      # Author of the book
    genre = db.Column(db.String(50), nullable=False)        # Genre of the book
    condition = db.Column(db.String(50), nullable=False)    # Condition of the book (e.g., New, Good, Fair)
    thumbnail = db.Column(db.String(200), nullable=False)   # URL to the book's thumbnail image
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    holder_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    possessed_since = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Convert the book object to a dictionary
    # This is useful for serializing the object to JSON for sending the data to the frontend from the backend,
    # which is used to show books on the frontend
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'condition': self.condition,
            'thumbnail': self.thumbnail, 
            'owner': User.query.get(self.owner_id).username if self.owner_id else None,
            'holder': User.query.get(self.holder_id).username if self.holder_id else None,
            'possessed_since': self.possessed_since.isoformat(), 
            'requests': [request.to_dict() for request in Request.query.filter_by(book_id=self.id).all()]
        }

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='open')  # open, accepted, return_initiated, completed
    requested_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    

    # Convert request to dict with its attributes
    def to_dict(self):
        # Get the book object directly from the database
        book = Book.query.get(self.book_id)
        return {
            'id': self.id,
            'book': {
                'title': book.title if book else None,
                'author': book.author if book else None,
                'genre': book.genre if book else None,
                'condition': book.condition if book else None,
                'thumbnail': book.thumbnail if book else None,
                'owner': {
                    'username': User.query.get(book.owner_id).username if book and book.owner_id else None
                },
                'holder': {
                    'username': User.query.get(book.holder_id).username if book and book.holder_id else None
                }
            },
            'requester': User.query.get(self.requester_id).username if self.requester_id else None,
            'requested_to': User.query.get(self.requested_to).username if self.requested_to else None,
            'holder': User.query.get(book.holder_id).username if book and book.holder_id else None,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'messages': [message.to_dict() for message in ChatMessage.query.filter_by(request_id=self.id).all()]
        }

# Chat message model
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sent_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'request_id': self.request_id,
            'sender': User.query.get(self.sender_id).username if self.sender_id else None,
            'sent_to': User.query.get(self.sent_to_id).username if self.sent_to_id else None,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }