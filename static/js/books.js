async function deleteBook(bookId) {
    const response = await fetch(`/api/book/${bookId}`, {
        method: 'DELETE'
    });
    const result = await response.json();
    if (result.ok) {
        alert('Book deleted successfully!');
        window.location.reload();
    } else {
        alert('Error deleting book: ' + result.error);
    }
}