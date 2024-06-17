import { debounce } from './debounce.js';

var game_data = null;

export function loadContent(url, data = null, replaceState = false) {
    // Ensure URL ends with a slash
    if (!url.endsWith('/')) {
        url += '/';
    }

    let fetchOptions = {
        headers: {
            'X-Requested-With': 'Fetch',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };

    // Add the language from localStorage to fetchOptions
    const language = localStorage.getItem('language');
    fetchOptions.headers['Content-Language'] = language;

    game_data = data;
    if (data) {
        fetchOptions.method = 'POST';
        fetchOptions.body = JSON.stringify(data);
		if (!url.endsWith('/')) {
			url += '/';
		}
    }

    fetch(url, fetchOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('content').innerHTML = html;
            if (replaceState) {
                history.replaceState(null, '', url);
            } else {
                history.pushState(null, '', url);
            }
            setupNavigationLinks();
            observeLanguageDropdown();
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
    loadContent('/initial_content/', null, true);

    window.addEventListener('popstate', function() {
        loadContent(location.pathname, null, true);
    });

    setupNavigationLinks();
    observeLanguageDropdown();
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

function observeLanguageDropdown() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && node.querySelector('.language-dropdown')) {
                    const dropdown = node.querySelector('.language-dropdown');
                    const currentLanguage = localStorage.getItem('language') || 'en';
                    dropdown.value = currentLanguage;
                    setupLanguageDropdown(dropdown);
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

function setupLanguageDropdown(dropdown) {
    dropdown.addEventListener('change', debounce(function() {
        const selectedLanguage = this.value;
        const currentLanguage = localStorage.getItem('language');
        if (selectedLanguage !== currentLanguage) {
            localStorage.setItem('language', selectedLanguage);
            const currentUrl = window.location.pathname;
            loadContent(currentUrl, null, true);
        }
    }, 300));
}