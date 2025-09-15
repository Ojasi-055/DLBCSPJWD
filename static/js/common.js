// Common functions for chat and request handling across books.html and requests.html

/**
 * Send a chat message for a specific request
 * @param {Event} event - The form submit event
 * @param {number} requestId - The ID of the request
 * @returns {boolean} - Always returns false to prevent form submission
 */
async function sendChat(event, requestId) {
    event.preventDefault();
    const input = document.getElementById(`msg-${requestId}`);
    const message = input.value.trim();
    
    if (!message) {
        alert('Please enter a message');
        return false;
    }

    try {
        const response = await fetch(`/request/${requestId}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ message: message })
        });

        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to send message');
            return false;
        }

        // Clear the input
        input.value = '';
        
        // Refresh the chat messages
        await loadChatMessages(requestId);
        
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Error sending message');
    }
    
    return false;
}

/**
 * Load chat messages for a specific request
 * @param {number} requestId - The ID of the request
 */
async function loadChatMessages(requestId) {
    try {
        const response = await fetch(`/request/${requestId}/chat`);
        const messages = await response.json();
        
        if (!response.ok) {
            console.error('Failed to load messages:', messages.error);
            return;
        }

        const chatDiv = document.getElementById(`chat-${requestId}`);
        if (!chatDiv) {
            console.error(`Chat div not found for request ${requestId}`);
            return;
        }

        // Clear existing messages
        chatDiv.innerHTML = '';
        
        // Add each message
        messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message';
            
            // Format the timestamp
            const date = new Date(message.created_at);
            const time = date.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit', 
                hour12: false 
            });
            
            messageDiv.innerHTML = `<strong>${message.sender}:</strong> ${message.message} <em>(${time})</em>`;
            chatDiv.appendChild(messageDiv);
        });
        
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

/**
 * Send a chat message from the owner's perspective (for books.html)
 * @param {Event} event - The form submit event
 * @param {number} requestId - The ID of the request
 * @returns {boolean} - Always returns false to prevent form submission
 */
async function sendOwnerChat(event, requestId) {
    return await sendChat(event, requestId);
}


/**
 * Accept a request
 * @param {number} requestId - The ID of the request to accept
 */
async function acceptRequest(requestId) {
    try {
        const response = await fetch(`/request/${requestId}/accept`, { 
            method: 'POST' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to accept request');
            return;
        }
        
        alert(data.message || 'Request accepted');
        window.location.reload();
        
    } catch (error) {
        console.error('Error accepting request:', error);
        alert('Error accepting request');
    }
}

/**
 * Reject a request
 * @param {number} requestId - The ID of the request to reject
 */
async function rejectRequest(requestId) {
    try {
        const response = await fetch(`/request/${requestId}/reject`, { 
            method: 'POST' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to reject request');
            return;
        }
        
        alert(data.message || 'Request rejected');
        window.location.reload();
        
    } catch (error) {
        console.error('Error rejecting request:', error);
        alert('Error rejecting request');
    }
}

/**
 * Complete a request
 * @param {number} requestId - The ID of the request to complete
 */
async function completeRequest(requestId) {
    try {
        const response = await fetch(`/request/${requestId}/complete`, { 
            method: 'POST' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to complete request');
            return;
        }
        
        alert(data.message || 'Request completed');
        window.location.reload();
        
    } catch (error) {
        console.error('Error completing request:', error);
        alert('Error completing request');
    }
}

/**
 * Transfer ownership of a book
 * @param {number} requestId - The ID of the request
 */
async function transferOwnership(requestId) {
    if (!confirm('Are you sure you want to transfer ownership of this book?')) {
        return;
    }

    try {
        const response = await fetch(`/request/${requestId}/transfer_ownership`, { 
            method: 'POST' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to transfer ownership');
            return;
        }
        
        alert(data.message || 'Ownership transferred');
        window.location.reload();
        
    } catch (error) {
        console.error('Error transferring ownership:', error);
        alert('Error transferring ownership');
    }
}

/**
 * Initiate return of a book
 * @param {number} requestId - The ID of the request
 */
async function initiateReturn(requestId) {
    try {
        const response = await fetch(`/request/${requestId}/initiate_return`, { 
            method: 'POST' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to initiate return');
            return;
        }
        
        alert(data.message || 'Return initiated');
        window.location.reload();
        
    } catch (error) {
        console.error('Error initiating return:', error);
        alert('Error initiating return');
    }
}

/**
 * Delete a request
 * @param {number} requestId - The ID of the request to delete
 */
async function deleteRequest(requestId) {
    if (!confirm('Are you sure you want to delete this request?')) {
        return;
    }

    try {
        const response = await fetch(`/request/${requestId}`, { 
            method: 'DELETE' 
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to delete request');
            return;
        }
        
        alert(data.message || 'Request deleted');
        window.location.reload();
        
    } catch (error) {
        console.error('Error deleting request:', error);
        alert('Error deleting request');
    }
}

/**
 * Request a book
 * @param {number} bookId - The ID of the book to request
 */
async function requestBook(bookId) {
    try {
        const response = await fetch(`/request_book/${bookId}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Request failed');
            return;
        }
        
        alert(data.message || 'Request sent successfully');
        
    } catch (error) {
        console.error('Error requesting book:', error);
        alert('Error requesting book');
    }
}