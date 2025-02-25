document.addEventListener('DOMContentLoaded', function() {
    var backToTopButton = document.getElementById("backToTop");

    function toggleBackToTopButton() {
        if (window.scrollY > 300) {
            backToTopButton.classList.add("show");
        } else {
            backToTopButton.classList.remove("show");
        }
    }

    window.addEventListener("scroll", toggleBackToTopButton);

    backToTopButton.addEventListener("click", function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});