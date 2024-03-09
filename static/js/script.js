document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');
    registerBtn.addEventListener('click', () => {
        container.classList.add('active');
    });
    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');
    });
});


function togglePasswordVisibility() {
    var password_reg = document.getElementById("password-reg");
    var eyeicon = document.getElementById("eyeicon");
    var eyeicon_slash = document.getElementById("eyeicon-slash");
    var password_log = document.getElementById("password-log");
    var eyeicon_log = document.getElementById("eyeicon-log");
    var eyeicon_slash_log = document.getElementById("eyeicon-slash-log");

    if (password_reg.type == "password") {
        password_reg.type = "text";
        eyeicon_slash.style.display = "inline";
        eyeicon.style.display = "none";
    } else {
        password_reg.type = "password";
        eyeicon_slash.style.display = "none";
        eyeicon.style.display = "inline";
    }

    if (password_log.type == "password") {
        password_log.type = "text";
        eyeicon_slash_log.style.display = "inline";
        eyeicon_log.style.display = "none";
    } else {
        password_log.type = "password";
        eyeicon_slash_log.style.display = "none";
        eyeicon_log.style.display = "inline";
    }
}
