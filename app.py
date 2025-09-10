from flask import Flask, jsonify, redirect, render_template, request, url_for
from db import db
from models import Book, User

app = Flask(__name__)
# Configuration: Database URI and Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To suppress a warning
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

        return redirect(url_for('index'))

    # Render the login form
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        username = request.form['username']
        password = request.form['password']
        # Add your registration logic here
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    # Render the registration form
    return render_template('register.html')


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
            thumbnail=data['thumbnail']
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({'ok': True})
    if request.method == 'GET':
        return jsonify([book.to_dict() for book in Book.query.all()]);