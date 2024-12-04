# **Aplikasi Penjualan Motor**

Aplikasi ini merupakan sistem penjualan motor yang dibangun menggunakan Django Rest Framework. Proyek ini menyediakan API untuk manajemen motor, kategori motor, dan pengguna, dan role (admin, staff, view).

---

## **Fitur**

- **Manajemen Pengguna**: CRUD pengguna dengan peran admin, staff, dan view, serta kontrol akses berdasarkan peran.
- **Manajemen Motor**: CRUD data motor dan kategorinya, khususnya untuk admin dan staff.
- **Role-Based Access Control (RBAC)**: Pengguna dibatasi aksesnya sesuai dengan peran mereka (admin, staff, user).
- **API Terstruktur**: Endpoint API yang jelas dan terstruktur untuk memudahkan integrasi dengan aplikasi lain.

---

## **Gambar ERD**

Berikut adalah diagram ERD (Entity Relationship Diagram) yang menggambarkan hubungan antar entitas dalam sistem:

![ERD Diagram](ERD_Penjualan_Motor.drawio.png)

---

## **Gambar Class Diagram**

Berikut adalah diagram Class Diagram:

![ERD Diagram](ClassDiagram_Penjualan_Motor_Gambar.drawio.png)

---

## **Requirements**

Aplikasi ini membutuhkan beberapa dependensi yang tercantum dalam `requirements.txt`. Berikut adalah cara untuk menginstal semua dependensi yang diperlukan:

1. **Buat Virtual Environment**  
   Pastikan membuat dan mengaktifkan virtual environment untuk proyek ini agar menghindari konflik dengan package lain di pada sistem anda.

   ```bash
   python -m venv env
   source env/bin/activate  # Untuk MacOS/Linux
   env\Scripts\activate     # Untuk Windows
