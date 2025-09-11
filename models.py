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
            'owner': User.query.get(self.owner_id).username,
            'holder': User.query.get(self.holder_id).username,
            'possessed_since': self.possessed_since.isoformat() 
        }