// 🌙 Toggle Dark Mode and store preference
function toggleDarkMode() {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

// 🧠 Restore dark mode on page load
document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
    }

    // 📄 Show selected filename
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener("change", () => {
            const label = document.createElement("span");
            label.textContent = "📄 " + fileInput.files[0]?.name || "No file selected";
            label.style.display = "block";
            label.style.marginTop = "8px";
            label.style.fontSize = "0.9rem";
            fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
        });
    }

    // ⚡ Spinner on submit
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            const button = form.querySelector("button[type='submit']");
            if (button) {
                button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Forecasting...`;
                button.disabled = true;
            }
        });
    }

    // 🔽 Auto-scroll to result
    const resultCard = document.querySelector(".card img.forecast-plot");
    if (resultCard) {
        resultCard.scrollIntoView({ behavior: "smooth", block: "center" });
    }
});
