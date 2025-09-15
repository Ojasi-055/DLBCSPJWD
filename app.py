from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from db import db
from datetime import datetime, timezone
from models import Book, ChatMessage, Request, User

app = Flask(__name__)
# Configuration: Database URI and Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ojk055@bookbank_dlbcspjwd#IU2025'

# Initialize the database
db.init_app(app)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%H:%M'):
    return datetime.fromisoformat(value).strftime(format)


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
    book_objs = [book.to_dict() for book in books]
    return render_template('books.html', books=book_objs)

# Requests route
@app.route('/requests')
def requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    requests = Request.query.filter_by(requester_id=session['user_id']).all()
    request_objs = [request.to_dict() for request in requests]
    return render_template('requests.html', requests=request_objs)

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
        return jsonify({'ok': True, 'message': 'Book added successfully'})
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
    return jsonify({'ok': True, 'message': 'Book deleted successfully'})


@app.route('/request_book/<int:book_id>', methods=['POST'])
def request_book(book_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    book = Book.query.get_or_404(book_id)
    if book.owner_id == session['user_id']:
        return jsonify({'error': "You can't request your own book"}), 400
    existing = Request.query.filter_by(requester_id=session['user_id'], book_id=book_id).first()
    if existing:
        return jsonify({'message': 'Already requested'})
    req = Request(
        requester_id=session['user_id'],
        book_id=book_id,
        requested_to=book.owner_id
    )
    db.session.add(req)
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Request sent successfully'})

@app.route('/request/<int:req_id>', methods=['DELETE'])
def delete_request(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    user_id = session['user_id']
    book = Book.query.get(req.book_id)
    is_requester = (req.requester_id == user_id)
    is_owner = (book.owner_id == user_id) if book else False
    if not (is_requester or is_owner):
        return jsonify({'error': 'Only requester or owner can delete request'}), 403
    if is_requester and req.status not in ['open', 'rejected', 'completed']:
        return jsonify({'error': 'Requester can delete only while request is open or rejected or completed'}), 403
    ChatMessage.query.filter_by(request_id=req.id).delete()
    db.session.delete(req)
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Request deleted'})

@app.route('/request/<int:req_id>/accept', methods=['POST'])
def accept_request(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if not book or book.owner_id != session['user_id']:
        return jsonify({'error': 'Only owner can accept'}), 403
    req.status = 'accepted'
    book.holder_id = req.requester_id
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Request accepted'})

@app.route('/request/<int:req_id>/reject', methods=['POST'])
def reject_request(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if not book or book.owner_id != session['user_id']:
        return jsonify({'error': 'Only owner can reject'}), 403
    req.status = 'rejected'
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Request rejected'})

@app.route('/request/<int:req_id>/initiate_return', methods=['POST'])
def initiate_return(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if req.requester_id != session['user_id'] and (not book or book.owner_id != session['user_id']):
        return jsonify({'error': 'Not allowed'}), 403
    req.status = 'return_initiated'
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Return initiated'})

@app.route('/request/<int:req_id>/complete', methods=['POST'])
def complete_request(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if req.requester_id != session['user_id'] and (not book or book.owner_id != session['user_id']):
        return jsonify({'error': 'Not allowed'}), 403
    req.status = 'completed'
    req.completed_at = datetime.now(timezone.utc)
    # Transfer book back to owner when completed
    if book:
        book.holder_id = book.owner_id
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Request completed'})

@app.route('/request/<int:req_id>/transfer_ownership', methods=['POST'])
def transfer_ownership(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if not book or book.owner_id != session['user_id']:
        return jsonify({'error': 'Only owner can transfer'}), 403
    # Transfer ownership of the book to the requester
    book.owner_id = req.requester_id
    book.holder_id = req.requester_id
    book.possessed_since = datetime.now(timezone.utc)
    req.status = 'completed'
    req.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Ownership transferred'})

@app.route('/request/<int:req_id>/chat', methods=['GET', 'POST'])
def request_chat(req_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in'}), 401
    req = Request.query.get_or_404(req_id)
    book = Book.query.get(req.book_id)
    if session['user_id'] not in [req.requester_id, book.owner_id if book else None]:
        return jsonify({'error': 'Not allowed'}), 403
    if request.method == 'POST':
        message = request.form.get('message') or (request.json.get('message') if request.is_json else None)
        if not message:
            return jsonify({'error': 'Message required'}), 400
        # Determine receiver
        sender_id = session['user_id']
        if sender_id == req.requester_id:
            receiver_id = book.owner_id if book else None
        else:
            receiver_id = req.requester_id
        chat = ChatMessage(request_id=req.id, sender_id=sender_id, sent_to_id=receiver_id, message=message)
        db.session.add(chat)
        db.session.commit()
        return jsonify({'ok': True, 'message': 'Message sent'})
    # GET
    return jsonify([{
        'id': m.id,
        'sender': User.query.get(m.sender_id).username if m.sender_id else None,
        'message': m.message,
        'created_at': m.created_at.isoformat()
    } for m in ChatMessage.query.filter_by(request_id=req.id).all()])
