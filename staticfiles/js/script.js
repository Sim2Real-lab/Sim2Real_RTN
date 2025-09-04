document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".toggle-password");

    toggles.forEach(toggle => {
        const input = document.querySelector(toggle.getAttribute("data-toggle"));
        const icon = toggle.querySelector("i");

        if (!input || !icon) return;

        // Toggle password visibility on click
        toggle.addEventListener("click", function () {
            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            icon.classList.toggle("fa-eye");
            icon.classList.toggle("fa-eye-slash");
        });

        // Show/hide toggle icon based on input focus or content
        const updateVisibility = () => {
            if (document.activeElement === input || input.value.length > 0) {
                toggle.style.display = "block";
            } else {
                toggle.style.display = "none";
            }
        };

        input.addEventListener("focus", updateVisibility);
        input.addEventListener("input", updateVisibility);
        input.addEventListener("blur", updateVisibility);
        updateVisibility();
    });
});
