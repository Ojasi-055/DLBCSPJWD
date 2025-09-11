  // Request book (placeholder)
  async function requestBook(bookId) {
    try {
      const response = await fetch(`/request_book/${bookId}`, {
        method: 'POST'
      });
      const result = await response.json();
      if (!response.ok) {
        alert(result.error || 'Request failed');
        return;
      }
      alert(result.message);
    } catch (error) {
      console.error('Error requesting book:', error);
      alert('Error requesting book');
    }
  }
