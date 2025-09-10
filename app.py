from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuration: Database URI and Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To suppress a warning
app.config['SECRET_KEY'] = 'ojk055@bookbank_dlbcspjwd#IU2025'
# Initialize the database
db = SQLAlchemy(app)

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
