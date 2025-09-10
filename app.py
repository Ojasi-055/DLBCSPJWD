from flask import Flask, jsonify, render_template, request
from db import db
from models import Book

app = Flask(__name__)
# Configuration: Database URI and Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To suppress a warning
app.config['SECRET_KEY'] = 'ojk055@bookbank_dlbcspjwd#IU2025'

# Initialize the database
db.init_app(app)

# Routes

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Books route
@app.route('/books')
def books():
    return render_template('books.html')

# Requests routemodels.py
@app.route('/requests')
def requests():
    return render_template('requests.html')


# Route for adding a book
@app.route('/api/books', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        data = request.form
        book = Book(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            condition=data['condition'],
            thumbnail=data['thumbnail']
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({'ok': True})
    if request.method == 'GET':
        return jsonify([book.to_dict() for book in Book.query.all()]);


