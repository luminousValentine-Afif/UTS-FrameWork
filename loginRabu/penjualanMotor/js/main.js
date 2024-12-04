document.addEventListener("DOMContentLoaded", async () => {
  const ACCESS_CONTROL = {
    admin: [],
    staf: ["#penggunaDropdown",
      "#duaAksiUser",
      "#tambah_user",
      "#aksiUser",
    ],
    user: [
      "#penggunaDropdown",
      "#storeDropdown",
      "#tambah_motor",
      "#aksi",
      "#duaAksiMotor",
      "#tambah_user",
      ".duaAksi",
      "#tambah_kategori",
      "#aksiKategorinya",
      "#duaAksiKategorii",
    ],
  };

  try {
    const auth = await userAccess();
    applyAccessControl(auth.access_level);
  } catch (error) {
    applyAccessControl()
    console.error("Error mendapatkan akses pengguna:", error);
  }

  /**
   * Mengatur kontrol akses berdasarkan level akses.
   * @param {number} accessLevel - Level akses pengguna.
   */
  
  
  function applyAccessControl(accessLevel) {
    switch (accessLevel) {
      case 1: // Admin, semua akses terbuka
      break;
      case 2: // Staf, batasi akses tertentu
      hideElements(ACCESS_CONTROL.staf);
      break;
      default: // User, batasi akses lebih banyak
        hideElements(ACCESS_CONTROL.user);
        break;
    }
  }

  /**
   * Menyembunyikan elemen berdasarkan selector atau NodeList.
   * @param {string[]|NodeList} selectors - Daftar selector atau NodeList.
   */
  function hideElements(selectors) {
    selectors.forEach((selector) => {
      const elements =
        typeof selector === "string"
          ? document.querySelectorAll(selector)
          : selector;

      if (elements instanceof NodeList) {
        elements.forEach((element) => removeElement(element));
      } else {
        removeElement(elements);
      }
    });
  }

  /**
   * Menghapus elemen dari DOM dengan pengecekan aman.
   * @param {Element} element - Elemen DOM yang akan dihapus.
   */
  function removeElement(element) {
    try {
      element?.remove();
    } catch (error) {
      console.error("Error menghapus elemen:", error);
    }
  }
});
