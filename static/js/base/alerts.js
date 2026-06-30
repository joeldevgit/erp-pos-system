document.addEventListener("DOMContentLoaded", function () {

    setTimeout(() => {

        document.querySelectorAll(".toast-message").forEach(toast => {

            toast.style.transition = "opacity .5s ease, transform .5s ease";
            toast.style.opacity = "0";
            toast.style.transform = "translateY(-10px)";

            setTimeout(() => {
                toast.remove();
            }, 500);

        });

    }, 3000);

});