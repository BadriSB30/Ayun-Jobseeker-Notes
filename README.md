# 📋 Jobseeker Note System

Aplikasi desktop untuk mencatat dan mengelola lamaran pekerjaan secara terorganisir menggunakan PyQt5 dengan penyimpanan lokal berbasis SQLite, pickle dan ekspor Excel via openpyxl.

## Struktur File

```
jobseeker_note_system/
├── main.py              # Entry point & jendela utama
├── config_db.py         # Konfigurasi database SQLite dan Pickle
├── styles.py            # Style aplikasi
├── build.spec           # Code untuk build aplikasi
├── assets/              # Ikon dan gambar aplikasi
│   └── favicon.ico
└── requirements.txt     # Dependensi Python
```

## Instalasi & Menjalankan

### 1. Buat Virtual Environment

```bash
python -m venv .venv
```

### 2. Aktifkan Virtual Environment

**Windows:**

```bash
source .venv/Scripts/activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

> Setelah aktif, prompt terminal akan berubah menjadi `(.venv) ...`

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python main.py
```

### 5. Menonaktifkan Virtual Environment (selesai pakai)

```bash
deactivate
```

---

## Fitur

### Catat Lamaran Kerja

- Tambah, edit, dan hapus data lamaran pekerjaan
- Simpan informasi: nama perusahaan, posisi, tanggal, status, dan catatan
- Penyimpanan otomatis ke file lokal `.pkl`

### Kelola & Filter Data

- Tampilkan semua lamaran dalam bentuk tabel
- Filter berdasarkan status lamaran (Pending, Interview, Accepted, Rejected)
- Pencarian cepat berdasarkan nama perusahaan atau posisi

### Ekspor Data

- Export seluruh data lamaran ke format Excel (`.xlsx`)
- Format tabel rapi dan siap cetak

---

## Penyimpanan Data

Data lamaran disimpan secara lokal di komputer pengguna:

```
C:\Users\<NamaUser>\jobseeker_notes.pkl
```

- Data **tidak dikirim** ke internet — sepenuhnya tersimpan lokal
- Disarankan **backup file `.pkl`** secara berkala ke tempat lain
- Tiap komputer memiliki data masing-masing (tidak tersinkronisasi)

---

## Build — Compile ke Executable

Gunakan **PyInstaller** yang sudah termasuk di `requirements.txt`.

### Kenapa `--add-data` wajib disertakan?

Saat `--onefile`, PyInstaller mengekstrak semua file ke folder sementara
`sys._MEIPASS` di runtime — **bukan** di samping `.exe`. Tanpa `--add-data`,
folder `assets/` tidak ikut terbundle dan ikon tidak muncul.

`main.py` sudah menggunakan fungsi `resource_path()` yang otomatis mengarah
ke `sys._MEIPASS` saat berjalan dari build, dan ke folder proyek saat
berjalan dari source.

### Perintah Build

**Windows** — menghasilkan `.exe` satu file:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/favicon.ico --add-data "assets;assets" --name="Jobseeker Note System" main.py
```

**macOS / Linux** — menghasilkan binary satu file:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/favicon.ico --add-data "assets:assets" --name="Jobseeker Note System" main.py
```

> Hasil build ada di folder `dist/Jobseeker Note System.exe` (Windows) atau `dist/Jobseeker Note System` (macOS/Linux).

### Penjelasan Flag

| Flag                             | Keterangan                                                                                                           |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `--onefile`                      | Semua dependensi dikemas dalam **satu file** executable                                                              |
| `--windowed`                     | Jalankan tanpa jendela terminal/console (mode GUI)                                                                   |
| `--icon=assets/favicon.ico`      | Ikon pada file `.exe` di File Explorer / Finder                                                                      |
| `--add-data "assets;assets"`     | **Bundel** folder `assets/` ke dalam `.exe` agar ikon muncul saat runtime (Windows pakai `;`, macOS/Linux pakai `:`) |
| `--name="Jobseeker Note System"` | Nama file output                                                                                                     |
| `--noconfirm`                    | Timpa folder `dist/` tanpa konfirmasi                                                                                |

### Membersihkan Hasil Build

```bash
rm -rf build/ dist/ "Jobseeker Note System.spec"
```

---

## Menggunakan File .spec (Opsional)

Untuk konfigurasi build lebih lanjut, tersedia file `.spec` yang sudah dikonfigurasi dengan optimasi:

- Library berat seperti `pandas`, `numpy`, `matplotlib` dikeluarkan agar hasil build lebih kecil
- UPX compression diaktifkan
- Folder `assets/` otomatis ikut terbundle

```bash
pyinstaller build.spec
```

---

## Catatan

- Folder `.venv` tidak perlu di-commit ke Git — tambahkan `.venv/` ke `.gitignore`
- File hasil build bersifat **portable** — tidak perlu instalasi di komputer lain
- Untuk menghapus aplikasi: hapus folder hasil extract + file `.pkl` di folder user
- Aplikasi hanya kompatibel dengan OS yang sama saat build (Windows → Windows)
