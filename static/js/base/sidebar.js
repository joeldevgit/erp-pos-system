document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.querySelector(".topbar-menu");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".overlay");

    if (!menuBtn || !sidebar || !overlay) return;

    menuBtn.addEventListener("click", function () {
        sidebar.classList.toggle("show");
        overlay.classList.toggle("show");
        document.body.classList.toggle("sidebar-open");
    });

    overlay.addEventListener("click", function () {
        sidebar.classList.remove("show");
        overlay.classList.remove("show");
        document.body.classList.remove("sidebar-open");
    });
});