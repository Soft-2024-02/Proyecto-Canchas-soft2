document.addEventListener("DOMContentLoaded", function () {
    var toastEl = document.getElementById('liveToast');
    
    if (toastEl) {
        var toast = new bootstrap.Toast(toastEl, { delay: 5000 });
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', function () {
            toastEl.remove();
        });
    }
});
