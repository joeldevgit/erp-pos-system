document.addEventListener("DOMContentLoaded", function () {

    const logoutBtn = document.getElementById("logoutBtn");

    if (!logoutBtn) return;

    logoutBtn.addEventListener("click", function () {

        const isDark = document.body.classList.contains("dark-mode");

        Swal.fire({
            title: '¿Cerrar sesión?',
            text: "Tu sesión actual se cerrará",
            icon: 'warning',
            background: isDark ? '#2a2a3c' : '#ffffff',
            color: isDark ? '#e4e6eb' : '#212529',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sí, cerrar sesión',
            cancelButtonText: 'Cancelar'
        }).then((result) => {

            if (result.isConfirmed) {

                Swal.fire({
                    title: 'Cerrando sesión...',
                    timer: 1000,
                    showConfirmButton: false,
                    background: isDark ? '#2a2a3c' : '#ffffff',
                    color: isDark ? '#e4e6eb' : '#212529'
                }).then(() => {
                    document.getElementById("logoutForm").submit();
                });

            }

        });

    });

});