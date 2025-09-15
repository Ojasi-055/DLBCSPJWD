# BookBank - Book Sharing Platform

**By Ojasi Kulkarni**

A Flask-based web application that allows users to share books with each other, manage book requests, and communicate through an integrated chat system.

## 📚 Project Overview

BookBank is a community-driven book sharing platform where users can:
- Add books to their personal library
- Browse and request books from other users
- Manage book requests (accept, reject, complete)
- Transfer book ownership
- Chat with other users about book requests
- Track book possession history

## 🏗️ Project Structure

```
DLBCSPJWD/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Book, Request, ChatMessage)
├── db.py                  # Database configuration
├── bookbank.py           # Additional utilities
├── instance/
│   └── bookbank.db       # SQLite database
├── static/
│   ├── styles.css        # CSS styling
│   ├── default.png       # Default book thumbnail
│   └── js/
│       ├── index.js      # Home page functionality
│       ├── books.js      # Book management functions
│       └── common.js     # Shared functions for chat and requests
└── templates/
    ├── index.html        # Home page with book listing
    ├── books.html        # User's book management page
    ├── requests.html     # User's request management page
    ├── login.html        # User authentication
    └── register.html     # User registration
```

## 🗄️ Database Models

### User Model
- **Fields**: `id`, `username`, `password`
- **Purpose**: Stores user account information
- **Relationships**: Owns books, makes requests, sends/receives messages

### Book Model
- **Fields**: `id`, `title`, `author`, `genre`, `condition`, `thumbnail`, `owner_id`, `holder_id`, `possessed_since`
- **Purpose**: Represents books in the system
- **Features**: Tracks ownership and current possession

### Request Model
- **Fields**: `id`, `requester_id`, `book_id`, `created_at`, `status`, `requested_to`, `completed_at`
- **Purpose**: Manages book borrowing requests
- **Status Flow**: `open` → `accepted` → `return_initiated` → `completed`

### ChatMessage Model
- **Fields**: `id`, `request_id`, `sender_id`, `sent_to_id`, `message`, `created_at`
- **Purpose**: Enables communication between users about book requests

## 🚀 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Main Pages
- `GET /` - Home page (requires authentication)
- `GET /books` - User's books page
- `GET /requests` - User's requests page

### Book Management
- `GET /api/books` - Fetch all available books
- `POST /api/books` - Add a new book
- `DELETE /api/book/<id>` - Delete a book (owner only)

### Request Management
- `POST /request_book/<book_id>` - Request a book
- `DELETE /request/<request_id>` - Delete a request
- `POST /request/<request_id>/accept` - Accept a request
- `POST /request/<request_id>/reject` - Reject a request
- `POST /request/<request_id>/complete` - Mark request as completed
- `POST /request/<request_id>/transfer_ownership` - Transfer book ownership
- `POST /request/<request_id>/initiate_return` - Initiate book return

### Chat System
- `GET /request/<request_id>/chat` - Get chat messages
- `POST /request/<request_id>/chat` - Send a chat message

## 💻 JavaScript Functions

### index.js (Home Page)
- **`addBook(event)`** - Handles book addition form submission
- **`fetchBooks()`** - Fetches and displays all available books
- **Features**: Form validation, error handling, dynamic book listing

### books.js (Book Management)
- **`deleteBook(bookId)`** - Deletes a book with confirmation
- **Features**: User confirmation, error handling, page reload

### common.js (Shared Functions)
- **Chat Functions**:
  - `sendChat(event, requestId)` - Send chat message
  - `sendOwnerChat(event, requestId)` - Send message from owner perspective
  - `loadChatMessages(requestId)` - Load and display chat messages

- **Request Management**:
  - `acceptRequest(requestId)` - Accept a book request
  - `rejectRequest(requestId)` - Reject a book request
  - `completeRequest(requestId)` - Mark request as completed
  - `transferOwnership(requestId)` - Transfer book ownership
  - `initiateReturn(requestId)` - Initiate book return
  - `deleteRequest(requestId)` - Delete a request
  - `requestBook(bookId)` - Request a book

## 🎯 Key Features

### 1. **Book Sharing System**
- Users can add books to their library
- Browse all available books in the community
- Request books from other users
- Track book possession and ownership

### 2. **Request Management**
- Complete request lifecycle management
- Status tracking (open, accepted, return_initiated, completed)
- Owner and requester can manage requests
- Automatic book holder updates

### 3. **Chat Integration**
- Real-time communication between users
- Chat history for each request
- Message timestamps and sender identification
- Seamless integration with request management

### 4. **Ownership Transfer**
- Permanent ownership transfer option
- Temporary borrowing with return functionality
- Possession tracking with timestamps

### 5. **User Authentication**
- Secure login/registration system
- Session management
- Protected routes and API endpoints

## 🔧 Technical Benefits

### 1. **Modular Architecture**
- **Separation of Concerns**: Clear separation between models, views, and controllers
- **Reusable Components**: Shared JavaScript functions across multiple pages
- **Scalable Structure**: Easy to add new features and endpoints

### 2. **Database Design**
- **No Relationships**: Direct queries instead of SQLAlchemy relationships for better control
- **Efficient Queries**: Optimized data access patterns
- **Data Integrity**: Proper foreign key constraints and validation

### 3. **Frontend-Backend Synchronization**
- **Consistent API Responses**: Standardized success/error response formats
- **Error Handling**: Comprehensive error handling in both frontend and backend
- **Real-time Updates**: Dynamic content updates without page refreshes

### 4. **User Experience**
- **Responsive Design**: Works across different devices
- **Intuitive Interface**: Clear navigation and user flows
- **Feedback Systems**: User confirmations and success/error messages

### 5. **Security Features**
- **Authentication Required**: Protected routes and API endpoints
- **Authorization Checks**: Users can only manage their own books/requests
- **Input Validation**: Form validation and sanitization

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy

### Installation
1. Clone the repository
2. Install dependencies: `pip install flask flask_sqlalchemy` or `pip install -r requirements.txt`
3. Run the application: `python bookbank.py`
4. Access the application at `http://localhost:5000` by default

### Usage
1. Register a new account or login
2. Add books to your library
3. Browse and request books from other users
4. Manage incoming requests
5. Chat with other users about book requests

## 📈 Future Enhancements

- **Search and Filtering**: Advanced book search capabilities
- **Rating System**: User and book rating system
- **Notifications**: Real-time notifications for requests and messages
- **Mobile App**: Native mobile application
- **Book Categories**: Enhanced categorization and tagging
- **Analytics**: Usage statistics and insights

## 🤝 Contributing

This project demonstrates modern web development practices with Flask, including:
- RESTful API design
- Database modeling without ORM relationships
- Frontend-backend synchronization
- User authentication and authorization
- Real-time communication features

---

**Developed by Ojasi Kulkarni**  
*DLBCSPJWD Project*