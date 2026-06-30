document.addEventListener("DOMContentLoaded", function () {

    const themeToggle = document.getElementById("themeToggle");
    const themeToggleMobile = document.getElementById("themeToggleMobile");

    function cambiarTema() {

        document.body.classList.toggle("dark-mode");

        const isDark = document.body.classList.contains("dark-mode");

        if (themeToggle) {
            themeToggle.textContent = isDark ? "☀️" : "🌙";
        }

        if (themeToggleMobile) {
            themeToggleMobile.innerHTML = isDark
                ? '<i class="bi bi-sun"></i> Modo claro'
                : '<i class="bi bi-moon"></i> Modo oscuro';
        }
    }

    themeToggle?.addEventListener("click", cambiarTema);
    themeToggleMobile?.addEventListener("click", cambiarTema);

});