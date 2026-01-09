// static/js/blog_list.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("search-form");
  const results = document.getElementById("blog-results");

  if (!form || !results) return;

  // Intercept search form submit
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Get query parameters from form
    const params = new URLSearchParams(new FormData(form));

    fetch(`?${params.toString()}`, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(res => res.text())
      .then(html => {
        results.innerHTML = html;
        // Update URL without reload
        history.pushState(null, "", `?${params.toString()}`);
      });
  });

  // Intercept pagination clicks inside blog-results
  results.addEventListener("click", (e) => {
    const link = e.target.closest(".pagination a");
    if (!link) return;

    e.preventDefault();

    fetch(link.href, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(res => res.text())
      .then(html => {
        results.innerHTML = html;
        history.pushState(null, "", link.href);
      });
  });

  // Handle browser back/forward buttons
  window.addEventListener("popstate", () => {
    fetch(location.search, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(res => res.text())
      .then(html => {
        results.innerHTML = html;
      });
  });
});
