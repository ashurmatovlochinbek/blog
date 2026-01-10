// static/js/hamburger-mobile.js

const toggle = document.getElementById('mobileMenuToggle');
const sidebar = document.querySelector('.sidebar');

// Toggle menu when clicking hamburger
toggle.addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent click from bubbling
    sidebar.classList.toggle('active');
    toggle.classList.toggle('active');
    
    // Change icon: ☰ (hamburger) ↔ × (close)
    if (sidebar.classList.contains('active')) {
        toggle.textContent = '×';
    } else {
        toggle.textContent = '☰';
    }
});

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    if (sidebar.classList.contains('active') &&
        !sidebar.contains(event.target) &&
        event.target !== toggle) {
        sidebar.classList.remove('active');
        toggle.classList.remove('active');
        toggle.textContent = '☰'; // Reset to hamburger icon
    }
});

// Close menu when clicking any link inside sidebar (optional but nice UX)
const sidebarLinks = sidebar.querySelectorAll('a, button');
sidebarLinks.forEach(link => {
    link.addEventListener('click', function() {
        sidebar.classList.remove('active');
        toggle.classList.remove('active');
        toggle.textContent = '☰';
    });
});
