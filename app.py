from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from db import db
from datetime import datetime, timezone
from models import Book, User

app = Flask(__name__)
# Configuration: Database URI and Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ojk055@bookbank_dlbcspjwd#IU2025'

# Initialize the database
db.init_app(app)

# Routes

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form['username']
        password = request.form['password']
        # Look for the user in the database
        user = User.query.filter_by(username=username, password=password).first()
        # If user exists, store the name and id in session for further actions
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        # Return an error in case of failure
        return render_template('login.html', error='Invalid credentials')
    # Render the login form
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists in the database and reject user creation if it does
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        # Redirect to login page
        return redirect(url_for('login'))
    # Render the registration form
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    # Remove the user details from the session data for a fresh application experience
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Home route
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Books route
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    books = Book.query.filter_by(owner_id=session['user_id']).all()
    return render_template('books.html', books=books)

# Requests routemodels.py
@app.route('/requests')
def requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('requests.html')

# Route for checking users for development
@app.route('/users')
def users():
    return jsonify([{'id': user.id, 'username': user.username, 'password': user.password} for user in User.query.all()])

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
            thumbnail=data['thumbnail'],
            owner_id=session['user_id'],
            holder_id=session['user_id'],
            possessed_since=datetime.now(timezone.utc)
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({'ok': True})
    if request.method == 'GET':
        return jsonify([book.to_dict() for book in Book.query.all()]);

# Route for deleting a book
@app.route('/api/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    user = User.query.get(session['user_id'])

    if not book:
        return jsonify({'error': 'Book not found'})
    if book.owner_id != user.id:
        return jsonify({'error': 'Unauthorized'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'ok': True})

