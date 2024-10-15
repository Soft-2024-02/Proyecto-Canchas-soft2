document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.user-dropdown');
    const dropdownMenu = dropdown.querySelector('.dropdown-menu');
    dropdown.addEventListener('mouseenter', function () {
        dropdown.classList.add('show');
    });
    dropdownMenu.addEventListener('mouseenter', function () {
        dropdown.classList.add('show');
    });
    dropdown.addEventListener('mouseleave', function () {
        dropdown.classList.remove('show');
    });
});
