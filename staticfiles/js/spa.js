document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');

    // Handle navigation clicks
    document.body.addEventListener('click', e => {
        const link = e.target.closest('a[data-link]');
        if (link) {
            e.preventDefault();
            const url = link.getAttribute('href');
            navigateTo(url);
        }
    });

    // Handle back/forward browser buttons
    window.addEventListener('popstate', () => {
        loadContent(location.pathname);
    });

    // Initial load handled by server, but we might want to lazy load subsequent sections
    // For now, let's just handle navigation.
});

async function navigateTo(url) {
    history.pushState(null, null, url);
    await loadContent(url);
}

async function loadContent(url) {
    const app = document.getElementById('main-content');
    app.innerHTML = '<div class="flex justify-center items-center h-64"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>';

    try {
        // We assume the server returns a partial HTML if we add a header or query param
        // Creating a special endpoint pattern is also an option, e.g. /section/about
        // Let's stick to the URL but ask for X-Requested-With: XMLHttpRequest (standard Ajax)
        // Or we can use a custom header 'X-SPA-Request': 'true'

        const response = await fetch(url, {
            headers: {
                'X-SPA-Request': 'true'
            }
        });

        if (response.ok) {
            const html = await response.text();
            app.innerHTML = html;
            window.scrollTo(0, 0);
            initializeAnimations();
            if (typeof window.updateActiveNavLink === 'function') {
                window.updateActiveNavLink();
            }
        } else {
            app.innerHTML = '<h1>404 - Page Not Found</h1>';
        }
    } catch (error) {
        console.error('Error loading content:', error);
        app.innerHTML = '<h1>Error loading content</h1>';
    }
}

function initializeAnimations() {
    // Re-trigger scroll animations or other JS logic for the new content
    const elements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    });

    elements.forEach(el => observer.observe(el));
}
