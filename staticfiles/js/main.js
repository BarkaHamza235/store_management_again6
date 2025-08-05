// Store Manager - Scripts JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de l'application
    initializeApp();
});

function initializeApp() {
    // Gestion des alertes automatiques
    handleAlerts();

    // Animation des éléments
    animateElements();

    // Gestion du responsive
    handleResponsive();

    // Confirmation des actions destructives
    handleConfirmations();

    // Raccourcis clavier globaux
    handleGlobalKeyboardShortcuts();
}

// Gestion automatique des alertes
function handleAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');

    alerts.forEach(alert => {
        // Animation d'entrée
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(-20px)';

        setTimeout(() => {
            alert.style.transition = 'all 0.5s ease';
            alert.style.opacity = '1';
            alert.style.transform = 'translateX(0)';
        }, 100);

        // Fermeture automatique après 5 secondes pour les messages de succès
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(20px)';

                    setTimeout(() => {
                        if (alert && alert.parentNode) {
                            alert.remove();
                        }
                    }, 500);
                }
            }, 5000);
        }
    });
}

// Animation des éléments au scroll
function animateElements() {
    const cards = document.querySelectorAll('.card, .glass');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-in-out';
            }
        });
    });

    cards.forEach(card => {
        observer.observe(card);
    });
}

// Gestion responsive
function handleResponsive() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Fermeture automatique du sidebar sur mobile après clic
    if (window.innerWidth <= 768) {
        const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (sidebar) {
                    sidebar.classList.remove('show');
                }
            });
        });
    }
}

// Confirmation des actions destructives
function handleConfirmations() {
    const dangerButtons = document.querySelectorAll('.btn-danger, [data-confirm]');

    dangerButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Êtes-vous sûr de vouloir effectuer cette action ?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Raccourcis clavier globaux
function handleGlobalKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+/ pour afficher l'aide
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            showHelpModal();
        }

        // Echap pour fermer les modales
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Afficher l'aide
function showHelpModal() {
    // Créer une modale d'aide dynamique
    const helpContent = `
        <div class="modal fade" id="helpModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-question-circle me-2"></i>Aide
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6>Raccourcis clavier :</h6>
                        <ul>
                            <li><kbd>Ctrl</kbd> + <kbd>/</kbd> - Afficher cette aide</li>
                            <li><kbd>Esc</kbd> - Fermer les modales</li>
                            <li><kbd>F4</kbd> - Focus sur la recherche (page caisse)</li>
                            <li><kbd>F12</kbd> - Finaliser la vente (page caisse)</li>
                        </ul>
                        <h6>Navigation :</h6>
                        <ul>
                            <li>Utilisez les menus latéraux pour naviguer</li>
                            <li>Les notifications se ferment automatiquement</li>
                            <li>Confirmez les actions destructives</li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Supprimer l'ancienne modale si elle existe
    const existingModal = document.getElementById('helpModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Ajouter la nouvelle modale
    document.body.insertAdjacentHTML('beforeend', helpContent);
    const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
    helpModal.show();
}

// Utilitaires pour les formulaires
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }
    });

    return isValid;
}

// Fonction pour afficher les notifications toast
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    // Créer un conteneur de toast s'il n'existe pas
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Ajouter le toast
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Supprimer le toast après fermeture
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Fonction globale pour confirmer la déconnexion
function confirmLogout() {
    return confirm('Êtes-vous sûr de vouloir vous déconnecter ?');
}

// Export des fonctions pour utilisation globale
window.showToast = showToast;
window.validateForm = validateForm;
window.confirmLogout = confirmLogout;
