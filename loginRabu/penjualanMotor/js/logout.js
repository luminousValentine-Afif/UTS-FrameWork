
function logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = "../login/login.html"; 
}

document.getElementById('logout').addEventListener('click', function(event) {
    event.preventDefault();
    logout();
});
