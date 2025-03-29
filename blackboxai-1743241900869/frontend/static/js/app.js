// Initialisation de l'application
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du thème (light/dark)
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // Initialisation des tooltips
    tippy('[data-tippy-content]', {
        arrow: true,
        animation: 'shift-away'
    });

    // Gestion des formulaires
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            
            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    body: new FormData(form)
                });
                
                if (!response.ok) throw new Error('Erreur réseau');
                const result = await response.json();
                
                if (result.redirect) {
                    window.location.href = result.redirect;
                } else if (result.success) {
                    showToast('Opération réussie', 'success');
                } else {
                    showToast(result.message || 'Erreur', 'error');
                }
            } catch (error) {
                showToast('Une erreur est survenue', 'error');
                console.error(error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
            }
        });
    });
});

// Fonction pour afficher les notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} fixed top-4 right-4 max-w-xs z-50 shadow-lg`;
    toast.innerHTML = `
        <div>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}