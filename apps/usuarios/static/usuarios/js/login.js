
function togglePassword() {
    const password = document.getElementById("password");
    const icon = document.getElementById("toggleIcon");

    if (password.type === "password") {
        password.type = "text";
        icon.classList.remove("bi-eye-fill");
        icon.classList.add("bi-eye-slash-fill");
    } else {
        password.type = "password";
        icon.classList.remove("bi-eye-slash-fill");
        icon.classList.add("bi-eye-fill");
    }
}

document.getElementById("loginForm").addEventListener("submit", function () {
    const btn = document.getElementById("btnLogin");
    const spinner = document.getElementById("btnSpinner");
    const text = document.getElementById("btnText");

    btn.disabled = true;
    spinner.classList.remove("d-none");
    text.textContent = "Ingresando...";
});
