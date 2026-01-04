// Main Application Initialization
import { authAPI, apiClient } from '../api/index.js';

// Check authentication and initialize app
async function init() {
    const app = document.getElementById('app');
    const authPage = document.getElementById('authPage');
    const loading = document.getElementById('loading');

    // Show loading
    loading.classList.remove('hidden');

    // Check if user is authenticated
    if (apiClient.accessToken) {
        try {
            // Verify token by getting user data
            const user = await authAPI.getMe();
            showApp(user);
        } catch (error) {
            console.error('Authentication check failed:', error);
            showAuth();
        }
    } else {
        showAuth();
    }

    function showApp(user) {
        authPage.classList.add('hidden');
        app.classList.remove('hidden');
        loading.classList.add('hidden');
        
        // Initialize app components
        initNavigation();
        initAuth();
        loadDashboard();
    }

    function showAuth() {
        app.classList.add('hidden');
        authPage.classList.remove('hidden');
        loading.classList.add('hidden');
        initAuthForms();
    }

    function initAuthForms() {
        const loginForm = document.getElementById('loginFormElement');
        const registerForm = document.getElementById('registerFormElement');
        const showRegisterBtn = document.getElementById('showRegisterBtn');
        const showLoginBtn = document.getElementById('showLoginBtn');

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            try {
                await authAPI.login({ username, password });
                const user = await authAPI.getMe();
                showApp(user);
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        });

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('registerEmail').value;
            const username = document.getElementById('registerUsername').value;
            const full_name = document.getElementById('registerFullName').value;
            const password = document.getElementById('registerPassword').value;

            try {
                await authAPI.register({ email, username, full_name, password });
                alert('Registration successful! Please login.');
                document.getElementById('registerForm').classList.add('hidden');
                document.getElementById('loginForm').classList.remove('hidden');
            } catch (error) {
                alert('Registration failed: ' + error.message);
            }
        });

        showRegisterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('registerForm').classList.remove('hidden');
        });

        showLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('registerForm').classList.add('hidden');
            document.getElementById('loginForm').classList.remove('hidden');
        });
    }

    function initNavigation() {
        const navLinks = document.querySelectorAll('.nav-link[data-page]');
        const pages = document.querySelectorAll('.page');

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = link.dataset.page;
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Show selected page
                pages.forEach(p => p.classList.remove('active'));
                document.getElementById(`${pageId}Page`).classList.add('active');
            });
        });
    }

    function initAuth() {
        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await authAPI.logout();
            location.reload();
        });
    }

    async function loadDashboard() {
        // This would load dashboard data
        console.log('Loading dashboard...');
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
