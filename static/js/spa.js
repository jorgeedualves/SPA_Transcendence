export const loadContent = async (templateName) => {
    try {
        const response = await fetch(`/templates/${templateName}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${templateName}`);
        }
        const html = await response.text();
        const handler = document.getElementById('content');
        handler.innerHTML = html;

        // Executar scripts incluídos no conteúdo carregado
        const scripts = handler.querySelectorAll('script');
        scripts.forEach((script) => {
            const newScript = document.createElement('script');
            newScript.src = script.src;
            newScript.defer = script.defer;
            document.body.appendChild(newScript);
        });
    } catch (error) {
        console.error('Error loading content:', error);
        const handler = document.getElementById('content');
        handler.innerHTML = '<h1>Error loading content</h1>';
    }
};

const templateMap = {
    '/': 'home.html',
    '/login': 'login.html',
    '/options': 'options.html',
    '/account': 'account.html',
    '/pong': 'pong.html',
    // Adicione outras rotas conforme necessário
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

document.addEventListener('DOMContentLoaded', async function () {
    // Load the initial content based on authentication status
    const isAuthenticated = await checkAuthentication();
    const initialTemplate = isAuthenticated ? 'home.html' : 'account.html';
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