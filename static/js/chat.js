// document.addEventListener('DOMContentLoaded', () => {
//     const blogIdElement = document.getElementById('blog-id');
//     if (!blogIdElement) return;
//
//     const blogId = blogIdElement.value;
//     const messagesDiv = document.getElementById('chat-messages');
//     if (!messagesDiv) return;
//
//     let currentOffset = 0;
//     let isLoading = false;
//     let hasMore = true;
//
//     // === WebSocket Connection ===
//     const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
//     const socket = new WebSocket(`${wsProtocol}://${window.location.host}/ws/chat/${blogId}/`);
//
//     socket.onopen = () => {
//         console.log('✅ WebSocket connected');
//     };
//
//     socket.onerror = (error) => {
//         console.error('❌ WebSocket error:', error);
//     };
//
//     socket.onclose = () => {
//         console.log('🔌 WebSocket closed');
//     };
//
//     // Handle incoming real-time messages
//     socket.onmessage = function(e) {
//         try {
//             const data = JSON.parse(e.data);
//             appendMessage(data); // newest at bottom
//         } catch (err) {
//             console.error('Failed to parse message:', err);
//         }
//     };
//
//     // === Load initial (latest) messages ===
//     async function loadInitialMessages() {
//         try {
//             const response = await fetch(`/chat/api/chat/${blogId}/messages/?offset=0&limit=20`);
//             if (!response.ok) {
//                 throw new Error(`HTTP ${response.status}`);
//             }
//             const result = await response.json();
//
//             // DB returns: [newest, ..., older] → we want oldest first in UI
//             result.messages.reverse().forEach(msg => appendMessage(msg));
//
//             currentOffset = result.messages.length;
//             hasMore = result.has_more;
//
//             // Scroll to bottom
//             messagesDiv.scrollTop = messagesDiv.scrollHeight;
//         } catch (err) {
//             console.error('Failed to load initial messages:', err);
//             messagesDiv.innerHTML += '<p class="error">Failed to load chat history.</p>';
//         }
//     }
//
//     // === Append message to BOTTOM (newest last) ===
//     function appendMessage(data) {
//         const messageEl = document.createElement('div');
//         messageEl.className = 'chat-message';
//         const time = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//         messageEl.innerHTML = `
//             <strong>${data.author_username}</strong>: ${data.content}
//             <small class="chat-timestamp">${time}</small>
//         `;
//         messagesDiv.appendChild(messageEl);
//     }
//
//     // === Load older messages on scroll-up ===
//     async function loadOlderMessages() {
//         if (isLoading || !hasMore) return;
//         isLoading = true;
//
//         try {
//             const response = await fetch(`/chat/api/chat/${blogId}/messages/?offset=${currentOffset}&limit=20`);
//             if (!response.ok) {
//                 throw new Error(`HTTP ${response.status}`);
//             }
//             const result = await response.json();
//
//             if (result.messages.length > 0) {
//                 // Older messages → prepend (appear above current content)
//                 result.messages.reverse().forEach(msg => {
//                     const el = document.createElement('div');
//                     el.className = 'chat-message';
//                     const time = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//                     el.innerHTML = `
//                         <strong>${msg.author_username}</strong>: ${msg.content}
//                         <small class="chat-timestamp">${time}</small>
//                     `;
//                     messagesDiv.prepend(el);
//                 });
//                 currentOffset += result.messages.length;
//                 hasMore = result.has_more;
//             } else {
//                 hasMore = false;
//             }
//         } catch (err) {
//             console.error('Failed to load older messages:', err);
//         } finally {
//             isLoading = false;
//         }
//     }
//
//     // === Scroll detection ===
//     function handleScroll() {
//         if (messagesDiv.scrollTop === 0 && hasMore && !isLoading) {
//             loadOlderMessages();
//         }
//     }
//
//     messagesDiv.addEventListener('scroll', handleScroll);
//
//     // === Send message ===
//     const input = document.getElementById('chat-message-input');
//     const sendBtn = document.getElementById('chat-send-btn');
//
//     function sendMessage() {
//         const text = input?.value?.trim();
//         if (text && socket.readyState === WebSocket.OPEN) {
//             socket.send(JSON.stringify({ message: text }));
//             input.value = '';
//         } else if (socket.readyState !== WebSocket.OPEN) {
//             console.warn('WebSocket is not open. Message not sent.');
//         }
//     }
//
//     sendBtn?.addEventListener('click', sendMessage);
//     input?.addEventListener('keypress', (e) => {
//         if (e.key === 'Enter') {
//             e.preventDefault(); // prevent form submission if inside form
//             sendMessage();
//         }
//     });
//
//     // === Start everything ===
//     loadInitialMessages();
// });

document.addEventListener('DOMContentLoaded', () => {
    const blogIdElement = document.getElementById('blog-id');
    const currentUserIdElement = document.getElementById('current-user-id');

    if (!blogIdElement || !currentUserIdElement) return;

    const blogId = blogIdElement.value;
    const currentUserId = parseInt(currentUserIdElement.value);
    const messagesDiv = document.getElementById('chat-messages');
    if (!messagesDiv) return;

    let currentOffset = 0;
    let isLoading = false;
    let hasMore = true;

    // === WebSocket Connection ===
    const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${wsProtocol}://${window.location.host}/ws/chat/${blogId}/`);

    socket.onopen = () => {
        console.log('✅ WebSocket connected');
    };

    socket.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
    };

    socket.onclose = () => {
        console.log('🔌 WebSocket closed');
    };

    // Handle incoming real-time messages
    socket.onmessage = function(e) {
        try {
            const data = JSON.parse(e.data);
            // Format timestamp for display
            const timeStr = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            appendMessage({
                id: data.id,
                author_id: data.author_id,
                username: data.author_username,
                content: data.content,
                timestamp: timeStr
            }, false); // false = not historical (new message)
        } catch (err) {
            console.error('Failed to parse message:', err);
        }
    };

    // === Load initial (latest) messages ===
    async function loadInitialMessages() {
        try {
            const response = await fetch(`/chat/api/chat/${blogId}/messages/?offset=0&limit=20`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const result = await response.json();

            // DB returns: [newest, ..., older] → we want oldest first in UI
            result.messages.reverse().forEach(msg => {
                const timeStr = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                appendMessage({
                    id: msg.id,
                    author_id: msg.author_id,
                    username: msg.author_username,
                    content: msg.content,
                    timestamp: timeStr
                }, true); // true = historical message
            });

            currentOffset = result.messages.length;
            hasMore = result.has_more;

            // Scroll to bottom after loading
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } catch (err) {
            console.error('Failed to load initial messages:', err);
            messagesDiv.innerHTML += '<p class="error">Failed to load chat history.</p>';
        }
    }

    // === NEW: Telegram-style appendMessage ===
    function appendMessage(msg, isHistorical = false) {
        const isOwn = msg.author_id === currentUserId;

        const div = document.createElement('div');
        div.classList.add('message', isOwn ? 'sent' : 'received');

        if (isOwn) {
            div.innerHTML = `
                <div class="message-text">${escapeHtml(msg.content)}</div>
                <div class="message-time">${msg.timestamp}</div>
            `;
        } else {
            div.innerHTML = `
                <div class="message-sender">${escapeHtml(msg.username)}</div>
                <div class="message-text">${escapeHtml(msg.content)}</div>
                <div class="message-time">${msg.timestamp}</div>
            `;
        }

        if (isHistorical) {
            // Prepend old messages (appear at top)
            messagesDiv.prepend(div);
        } else {
            // Append new messages (appear at bottom)
            messagesDiv.appendChild(div);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    }

    // === Load older messages on scroll-up ===
    async function loadOlderMessages() {
        if (isLoading || !hasMore) return;
        isLoading = true;

        try {
            const response = await fetch(`/chat/api/chat/${blogId}/messages/?offset=${currentOffset}&limit=20`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const result = await response.json();

            if (result.messages.length > 0) {
                // Older messages → prepend (appear above current content)
                result.messages.forEach(msg => {
                    const timeStr = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                    appendMessage({
                        id: msg.id,
                        author_id: msg.author_id,
                        username: msg.author_username,
                        content: msg.content,
                        timestamp: timeStr
                    }, true);
                });
                currentOffset += result.messages.length;
                hasMore = result.has_more;
            } else {
                hasMore = false;
            }
        } catch (err) {
            console.error('Failed to load older messages:', err);
        } finally {
            isLoading = false;
        }
    }

    // === Scroll detection ===
    function handleScroll() {
        if (messagesDiv.scrollTop === 0 && hasMore && !isLoading) {
            loadOlderMessages();
        }
    }

    messagesDiv.addEventListener('scroll', handleScroll);

    // === Send message ===
    const input = document.getElementById('chat-message-input');
    const sendBtn = document.getElementById('chat-send-btn');

    function sendMessage() {
        const text = input?.value?.trim();
        if (text && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ message: text }));
            input.value = '';
        } else if (socket.readyState !== WebSocket.OPEN) {
            console.warn('WebSocket is not open. Message not sent.');
        }
    }

    sendBtn?.addEventListener('click', sendMessage);
    input?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // === Start everything ===
    loadInitialMessages();
});

// === Helper: Escape HTML to prevent XSS ===
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, s => map[s]);
}