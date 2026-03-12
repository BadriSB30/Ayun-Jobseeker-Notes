# 📋 Jobseeker Note System

Aplikasi desktop untuk mencatat dan mengelola lamaran pekerjaan secara terorganisir, dibangun menggunakan **PyQt5** dengan penyimpanan lokal berbasis **SQLite** dan pengelolaan konfigurasi menggunakan **pickle**. Aplikasi juga mendukung ekspor data ke format Excel melalui `openpyxl`.

---

## 🚀 Fitur

### 1. Catat Lamaran Kerja

Tambah, edit, dan hapus data lamaran pekerjaan dengan informasi lengkap, meliputi:

- Nama perusahaan
- Posisi
- Platform lamaran
- Tipe pekerjaan
- Status lamaran
- Tanggal melamar
- Estimasi gaji

> Semua data disimpan secara lokal menggunakan **SQLite Database**.

### 2. Kelola & Filter Data

- Menampilkan seluruh lamaran dalam bentuk tabel
- Pencarian cepat berdasarkan nama perusahaan atau posisi
- Filter data berdasarkan status lamaran

### 3. Manajemen Opsi Dinamis

Pengguna dapat mengelola opsi-opsi berikut secara fleksibel:

- Platform lamaran (LinkedIn, JobStreet, dll.)
- Status lamaran
- Tipe pekerjaan

Opsi disimpan menggunakan **pickle** sehingga dapat dikustomisasi tanpa perlu mengubah kode program.

### 4. Ekspor Data

- Ekspor seluruh data lamaran ke format **Excel** (`.xlsx`)
- Tabel terformat rapi, siap digunakan untuk dokumentasi atau pelaporan

---

## 📂 Struktur Project

```
jobseeker_note_system/
├── main.py              # Entry point & GUI aplikasi
├── config_db.py         # Konfigurasi SQLite dan Pickle
├── styles.py            # Styling aplikasi
├── build.spec           # Konfigurasi build PyInstaller
├── assets/              # Ikon dan gambar aplikasi
│   └── favicon.ico
└── requirements.txt     # Dependensi Python
```

---

## ⚙️ Instalasi & Menjalankan

### 1. Buat Virtual Environment

```bash
python -m venv .venv
```

### 2. Aktifkan Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Jika berhasil, prompt terminal akan berubah menjadi:

```
(.venv)
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python main.py
```

### 5. Menonaktifkan Virtual Environment

```bash
deactivate
```

---

## 💾 Penyimpanan Data

Aplikasi menyimpan data secara lokal di komputer pengguna pada folder berikut:

```
~/.jobseeker_note/
```

Isi folder tersebut:

```
.jobseeker_note/
├── job_notes.db        # Database SQLite untuk data lamaran
└── job_options.pkl     # File konfigurasi opsi (pickle)
```

| File              | Fungsi                                                      |
| ----------------- | ----------------------------------------------------------- |
| `job_notes.db`    | Database SQLite yang menyimpan semua data lamaran           |
| `job_options.pkl` | Menyimpan opsi seperti platform, status, dan tipe pekerjaan |

### 🔒 Keamanan Data

- Data **tidak** dikirim ke internet
- Semua data tersimpan sepenuhnya di lokal
- Disarankan untuk melakukan backup folder `.jobseeker_note` secara berkala

---

## 🏗️ Build Aplikasi (Compile ke Executable)

Aplikasi dapat dikompilasi menjadi file `.exe` menggunakan **PyInstaller**.

Tersedia dua cara build — pilih salah satu sesuai kebutuhan.

---

### ✅ Cara 1 — Menggunakan `build.spec` (Direkomendasikan)

File `build.spec` sudah tersedia di project dan berisi seluruh konfigurasi build. Cukup jalankan:

```bash
pyinstaller build.spec
```

> Cara ini lebih bersih karena tidak menghasilkan file `.spec` baru dan seluruh konfigurasi build sudah terpusat di satu file.

---

### 🔧 Cara 2 — Menggunakan Perintah Manual (Tanpa `.spec`)

Gunakan cara ini jika ingin melakukan build secara langsung tanpa menggunakan file `build.spec`.

> ⚠️ PyInstaller akan otomatis membuat file `Jobseeker Note System.spec` baru di direktori project. File ini bisa diabaikan atau dihapus setelah build selesai.

**Windows:**

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/favicon.ico --add-data "assets;assets" --name="Jobseeker Note System" main.py
```

**macOS / Linux:**

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/favicon.ico --add-data "assets:assets" --name="Jobseeker Note System" main.py
```

#### Penjelasan Flag PyInstaller

| Flag          | Penjelasan                                              |
| ------------- | ------------------------------------------------------- |
| `--onefile`   | Mengemas semua dependensi dalam satu file executable    |
| `--windowed`  | Menjalankan aplikasi GUI tanpa membuka jendela terminal |
| `--icon`      | Menentukan ikon aplikasi                                |
| `--add-data`  | Menyertakan folder `assets` ke dalam build              |
| `--name`      | Menentukan nama file output                             |
| `--noconfirm` | Menimpa folder build tanpa meminta konfirmasi           |

---

### Hasil Build

Setelah build selesai (dengan cara apapun), file executable akan tersimpan di folder:

```
dist/
└── Jobseeker Note System.exe
```

---

## 🧹 Membersihkan Hasil Build

Untuk menghapus file hasil build:

```bash
rm -rf build dist *.spec
```

> ⚠️ Perintah `*.spec` akan menghapus **semua** file `.spec` di direktori saat ini, termasuk `build.spec`. Pastikan `build.spec` sudah ter-commit ke Git sebelum menjalankan perintah ini, atau hapus folder `build` dan `dist` secara manual tanpa menyertakan `*.spec`.

---

## 📌 Catatan

- Folder `.venv` **tidak** perlu di-commit ke Git — tambahkan `.venv/` ke `.gitignore`
- File `.exe` hasil build bersifat **portable**
- Aplikasi hanya kompatibel dengan sistem operasi yang sama saat proses build dilakukan

| Build di | Bisa dijalankan di |
| -------- | ------------------ |
| Windows  | Windows            |
| Linux    | Linux              |
| macOS    | macOS              |
