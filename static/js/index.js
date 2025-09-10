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
        form_data.set('thumbnail', 'default_thumbnail.jpg');
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
    } else {
        alert('Error adding book: ' + result.error);
    }
}

  // Event listeners
document.getElementById('add-book-form').addEventListener('submit', (e) => {
    // Prevent form submission
    e.preventDefault();
    // Run the addBook function
    addBook();
});
