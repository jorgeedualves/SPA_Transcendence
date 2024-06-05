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
                history.replaceState(null, '', url);
            } else {
                history.pushState(null, '', url);
            }
            setupNavigationLinks();
            loadScriptsDynamically();
        })
        .catch(error => console.error('Error loading content:', error));
}

function loadScriptsDynamically() {
    const scripts = document.querySelectorAll('script[data-src]');
    scripts.forEach(script => {
        const newScript = document.createElement('script');
        newScript.src = script.getAttribute('data-src');
        newScript.defer = true;
        document.body.appendChild(newScript);
    });
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
    loadContent('/initial_content/', true);

    window.addEventListener('popstate', function() {
        loadContent(location.pathname, true);
    });

    setupNavigationLinks();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
