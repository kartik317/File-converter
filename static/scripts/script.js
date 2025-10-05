document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'block';
            const btn = this.querySelector('button[type="submit"]');
            if (btn) btn.disabled = true;
        });
    });
});
