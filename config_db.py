# src/config_db.py
import sqlite3
from pathlib import Path
import pickle

APP_FOLDER = Path.home() / ".jobseeker_note"
APP_FOLDER.mkdir(parents=True, exist_ok=True)

DB_PATH = APP_FOLDER / "job_notes.db"
OPTIONS_PATH = APP_FOLDER / "job_options.pkl"

DEFAULT_OPTIONS = {
    "platforms": ["LinkedIn", "JobStreet", "Company Website", "Indeed", "Referral"],
    "statuses": ["Applied", "Interview", "Test", "Offer", "Rejected", "Waiting"],
    "job_types": ["Full Time", "Internship", "Contract"]
}

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Tambahkan kolom Type jika belum ada
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_notes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Company TEXT,
            Position TEXT,
            Platform TEXT,
            Salary TEXT,
            AppliedDate TEXT,
            Status TEXT,
            Type TEXT
        )
    """)
    # Jika tabel lama belum ada kolom Type, tambahkan
    cur.execute("PRAGMA table_info(job_notes)")
    columns = [c[1] for c in cur.fetchall()]
    if "Type" not in columns:
        cur.execute("ALTER TABLE job_notes ADD COLUMN Type TEXT DEFAULT 'Full Time'")
    conn.commit()
    conn.close()

def save_pickle(obj, path: Path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_pickle(path: Path, default=None):
    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return default
