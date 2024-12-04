function parseJwt() {
    var token = localStorage.getItem('access');
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(
        window.atob(base64)
            .split('')
            .map(function (c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join('')
    );
    return JSON.parse(jsonPayload);
}

async function userAccess () {
    const token = parseJwt()
    const auth = await fetch(`http://127.0.0.1:8000/api/user/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access')}`,
        },
    })
    .then(response => response.json())
    .then(data => {
        return data.find(item => item.id == token.user_id)
    })
    .catch(error => console.error('Error:', error));

    return auth
}