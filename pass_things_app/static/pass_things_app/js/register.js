document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('label').forEach(el => el.style.display = 'None');
    document.querySelectorAll('p input').forEach(el => el.parentElement.className = "form-group");
});
