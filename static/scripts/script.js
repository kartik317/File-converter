document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            var spinner = document.getElementById('loadingSpinner');
            if (spinner) spinner.style.display = 'block';
            var btn = this.querySelector('button[type="submit"]');
            if (btn) btn.disabled = true;
        });
    }
});
