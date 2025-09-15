// This file contains JavaScript code to handle dynamic features on the index page and function to delete book

/**
 * Add a book to the database
 * @param {Event} event - The form submit event
 */
async function addBook(event) {
    event.preventDefault();
    
    const form = document.getElementById('add-book-form');
    const form_data = new FormData(form);
    
    // Basic validation
    if (!form_data.get('title') || !form_data.get('condition')) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Set default thumbnail if none provided
    if (!form_data.get('thumbnail')) {
        form_data.set('thumbnail', 'default.png');
    }
    
    try {
        // Send data to the server
        const response = await fetch('/api/books', {
            method: 'POST',
            body: form_data
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to add book');
            return;
        }
        
        alert(data.message || 'Book added successfully!');
        form.reset();
        await fetchBooks();
        
    } catch (error) {
        console.error('Error adding book:', error);
        alert('Error adding book');
    }
}

/**
 * Fetch and display all books from the server
 */
async function fetchBooks() {
    try {
        const response = await fetch('/api/books');
        const books = await response.json();
        
        if (!response.ok) {
            console.error('Failed to fetch books:', books.error);
            return;
        }
        
        const bookList = document.getElementById('book-list');
        if (!bookList) {
            console.error('Book list element not found');
            return;
        }
        
        bookList.innerHTML = books.map(book => `
            <div class="book-card">
                <img src="${book.thumbnail}" alt="${book.title}" onerror="this.onerror=null;this.src='static/default.png';">
                <h3>${book.title}</h3>
                <p>Title: ${book.title}</p>
                <p>Condition: ${book.condition}</p>
                <p>Author: ${book.author}</p>
                <p>Genre: ${book.genre}</p>
                <p>Holder: ${book.holder}</p>
                <p>Owner: ${book.owner} | Since: ${book.possessed_since}</p>
                <button onclick="requestBook(${book.id})">Request Book</button>
            </div>
        `).join('');
        
        console.log('Books fetched and displayed.');
        
    } catch (error) {
        console.error('Error fetching books:', error);
    }
}

/**
 * Delete a book
 * @param {number} bookId - The ID of the book to delete
 */
async function deleteBook(bookId) {
    if (!confirm('Are you sure you want to delete this book?')) {
        return;
    }

    try {
        const response = await fetch(`/api/book/${bookId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to delete book');
            return;
        }
        
        alert(data.message || 'Book deleted successfully');
        window.location.reload();
        
    } catch (error) {
        console.error('Error deleting book:', error);
        alert('Error deleting book');
    }
}

// Event listeners
document.getElementById('add-book-form').addEventListener('submit', (e) => {
    addBook(e);
});

// Initialize book list when page loads
window.onload = fetchBooks;