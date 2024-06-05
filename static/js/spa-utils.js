export function loadContent(url, data = null, replaceState = false) {
    let fetchOptions = {
        headers: {
            'X-Requested-With': 'Fetch',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };

    if (data) {
        fetchOptions.method = 'POST';
        fetchOptions.body = JSON.stringify(data);
    }

    fetch(url, fetchOptions)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content').innerHTML = html;
            if (replaceState) {
                history.replaceState(null, '', url); // Replace URL
            } else {
                history.pushState(null, '', url); // Update browser URL
            }

            // Manually evaluate and execute script tags in the loaded content
            const scripts = document.getElementById('content').getElementsByTagName('script');
            for (let script of scripts) {
                eval(script.innerText);
            }

            // Call the setup function if defined
            if (typeof setup === 'function') {
                setup();
            }

            // Add event listeners to new navigation links after content is loaded
            setupNavigationLinks();
        })
        .catch(error => console.error('Error loading content:', error));
}

function setupNavigationLinks() {
    document.querySelectorAll('a[data-template]').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('href');
            loadContent(url);
        });
    });
}

export function initializeSPA() {
    // Initial load content
    loadContent('/initial_content/', true);

    // Handle browser navigation (back/forward buttons)
    window.addEventListener('popstate', function() {
        loadContent(location.pathname, true);
    });

    // Setup initial navigation links
    setupNavigationLinks();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}