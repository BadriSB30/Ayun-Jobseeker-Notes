# -*- mode: python ; coding: utf-8 -*-

"""
Build Spec untuk:
    Jobseeker Note System (PyQt5 + pickle + openpyxl)
Optimasi:
- Tanpa pandas (lebih ringan)
- Folder assets ikut bundle
- Database (.pkl) tetap di lokasi user HOME
"""

import os
from PyInstaller.utils.hooks import collect_submodules

# --- Konfigurasi Utama ---
app_name = "Jobseeker Note System"
entry_script = "main.py"
icon_file = os.path.join("assets", "favicon.ico")

# --- Data Tambahan ---
datas = [
    ("assets", "assets"),  # Bundle folder assets (ikon/gambar)
]

# --- Hidden Imports ---
hiddenimports = (
    collect_submodules("PyQt5") +
    collect_submodules("openpyxl") +
    collect_submodules("pyexcel") +
    collect_submodules("pyexcel_xlsx")
)

# --- Analisis ---
a = Analysis(
    [entry_script],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "PyQt6",
        "pandas",        # ⚠️ dikeluarkan (berat)
        "matplotlib",
        "scipy",
        "notebook",
        "test",
        "tests",
        "numpy",         # ⚠️ opsional jika tidak dipakai
    ],
    noarchive=False,
)

# --- Kompres Bytecode ---
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- EXE ---
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    strip=False,
    upx=True,           # aktifkan UPX agar hasil build lebih kecil
    console=False,
    icon=icon_file,
)

# --- Koleksi Final Build ---
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=app_name,
)
