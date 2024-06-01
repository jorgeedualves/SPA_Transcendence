document.addEventListener('DOMContentLoaded', async function () {
    const templateMap = {
        '/': 'home.html',
        '/login': 'authentication/login.html',
        '/dale': 'dale.html',
        '/game': 'game/game.html'
        // Adicione outras rotas conforme necessário
    };

    const loadContent = async (templateName) => {
        try {
            const response = await fetch(`/templates/${templateName}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch ${templateName}`);
            }
            const html = await response.text();
            const handler = document.getElementById('content');
            handler.innerHTML = html;
        } catch (error) {
            console.error('Error loading content:', error);
            const handler = document.getElementById('content');
            handler.innerHTML = '<h1>Error loading content</h1>';
        }
    };

    // Check if the user is authenticated
    const checkAuthentication = async () => {
        try {
            const response = await fetch('/api/check-authentication/');
            if (!response.ok) {
                throw new Error('Failed to check authentication');
            }
            const data = await response.json();
            return data.is_authenticated;
        } catch (error) {
            console.error('Error checking authentication:', error);
            return false;
        }
    };

    // Load the initial content based on authentication status
    const isAuthenticated = await checkAuthentication();
    const initialTemplate = isAuthenticated ? 'home.html' : 'login.html';
    loadContent(initialTemplate);

    // Adding event listeners for navigation links
    document.addEventListener('click', (e) => {
        const { target } = e;
        if (target.matches('nav a')) {
            e.preventDefault();
            const templateName = target.getAttribute('data-template');
            loadContent(templateName);
            window.history.pushState({}, '', target.getAttribute('href'));
        }
    });

    // Handling browser navigation (back/forward)
    window.onpopstate = () => {
        const path = window.location.pathname;
        const templateName = templateMap[path] || '404.html';
        loadContent(templateName);
    };
});
