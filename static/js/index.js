// This file contains JavaScript code to handle dynamic features on the index page

// Add a book in the database (Dynamic feature #1)
async function addBook(event) {
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
    // Send data to the server
    const response = await fetch('/api/books', {
        method: 'POST',
        body: form_data
    });
    // Handle response
    const result = await response.json();
    if (result.ok) {
        alert('Book added successfully!');
        form.reset();
        fetchBooks();
    } else {
        alert('Error adding book: ' + result.error);
    }
}

async function fetchBooks() {
    const response = await fetch('/api/books');
    const books = await response.json();
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = books.map(book => `
        <div class="book-card">
            <img src="${book.thumbnail}" alt="${book.title}" onerror="this.onerror=null;this.src='static/default.png';">            <h3>${book.title}</h3>
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
}


async function requestBook(bookId) {
    alert("Book requested");
}

// Event listeners
document.getElementById('add-book-form').addEventListener('submit', (e) => {
    // Prevent form submission
    e.preventDefault();
    // Run the addBook function
    addBook();
});


// Initialize book list
window.onload = fetchBooks;