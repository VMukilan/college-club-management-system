// College Club Management System - Client Application Scripts (v0.1)

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds if not closed manually
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(function () {
                    alert.remove();
                }, 500);
            }
        }, 5000);
    });

    // Simple confirmation for destructive or administrative actions
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            const message = button.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});
