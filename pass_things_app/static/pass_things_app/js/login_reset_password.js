document.addEventListener("DOMContentLoaded", function () {
    const resetPassword = document.createElement('a');
    resetPassword.innerText = "Przypomnij hasło";
    resetPassword.className = "btn btn--small btn--without-border reset-password";
    resetPassword.setAttribute('href', '#')
    document.querySelector('#id_password').parentElement.appendChild(resetPassword)
});
