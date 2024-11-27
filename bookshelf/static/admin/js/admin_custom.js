
document.querySelector("#sidebar-toggle").addEventListener("click", function () {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("open");
});


document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".fadeIn");
    elements.forEach(function (element) {
        element.classList.add("fadeIn");
    });
});
