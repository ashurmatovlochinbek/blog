// static/js/comments.js
// Initialize comments functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initCommentForm();
    initLoadMoreButton();
});

// AJAX Comment Submission
function initCommentForm() {
    const commentForm = document.getElementById('comment-form');
    if (!commentForm) return;

    commentForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const form = this;
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Posting...';

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove "no comments" message if present
                const noCommentsMsg = document.getElementById('no-comments-message');
                if (noCommentsMsg) {
                    noCommentsMsg.remove();
                }

                const commentsList = document.getElementById('comments-list');
                // Insert new comment at the TOP (newest first)
                commentsList.insertAdjacentHTML('afterbegin', data.html);

                // Get the newly added comment (it's the first child now)
                const newComment = commentsList.firstElementChild;

                // Update comment count
                document.getElementById('comment-count').textContent = data.comment_count;

                // Clear form
                form.reset();

                // Scroll to the new comment (force scroll to top of comment)
                if (newComment) {
                    newComment.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    // Highlight briefly
                    newComment.style.backgroundColor = '#ffffcc';
                    setTimeout(() => {
                        newComment.style.backgroundColor = '';
                    }, 2000);
                }

                showNotification('Comment posted successfully!');
            } else {
                alert('Error posting comment. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Post Comment';
        });
    });
}

// Load More Comments
function initLoadMoreButton() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (!loadMoreBtn) return;

    loadMoreBtn.addEventListener('click', function () {
        const btn = this;
        const nextPage = btn.dataset.nextPage;
        const blogPk = btn.dataset.blogPk;

        btn.disabled = true;
        btn.textContent = 'Loading...';

        fetch(`/blog/${blogPk}/?page=${nextPage}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => {
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new TypeError("Response is not JSON!");
            }
            return response.json();
        })
        .then(data => {
            const commentsList = document.getElementById('comments-list');
            // Append older comments to the BOTTOM
            commentsList.insertAdjacentHTML('beforeend', data.html);

            if (data.has_next) {
                btn.dataset.nextPage = data.next_page;
                btn.disabled = false;
                btn.textContent = 'Load More Comments';
            } else {
                btn.parentElement.remove();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load more comments. Please try again.');
            btn.disabled = false;
            btn.textContent = 'Load More Comments';
        });
    });
}

// Notification System
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}