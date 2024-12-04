document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access'); // Ambil token dari localStorage

    if (!token) {
        document.getElementById('user-greeting').textContent = 'Halo, Guest';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/user-profile/', { // Ganti endpoint sesuai kebutuhan
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Gagal mengambil data pengguna');
        }

        const data = await response.json(); // Data dari API
        const username = data.username || 'Pengguna';
        const role = data.access_level?.nama_role || 'Tidak diketahui';

        document.getElementById('user-greeting').textContent = `Halo ${role}, ${username}`;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        document.getElementById('user-greeting').textContent = 'Halo, Pengguna';
    }
});
