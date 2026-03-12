import sys
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QMessageBox, QListWidget, QInputDialog, QHeaderView, QFileDialog
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QDate
from PyQt5.QtGui import QIcon
from config_db import init_db, get_connection, OPTIONS_PATH, DEFAULT_OPTIONS, save_pickle, load_pickle
from styles import APP_STYLE
import openpyxl


# ---------- Helper ----------
def load_options():
    opts = load_pickle(OPTIONS_PATH, default=None)
    if opts is None:
        opts = DEFAULT_OPTIONS.copy()
        save_pickle(opts, OPTIONS_PATH)
    else:
        if "job_types" not in opts:
            opts["job_types"] = DEFAULT_OPTIONS["job_types"]
            save_pickle(opts, OPTIONS_PATH)
    return opts


def fetch_all_jobs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM job_notes ORDER BY ID DESC")
    rows = cur.fetchall()
    conn.close()
    cols = [col[0] for col in cur.description]
    return [dict(zip(cols, row)) for row in rows]


# ---------- Model ----------
class SQLiteTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.headers = ["Company", "Position", "Type", "Platform", "Salary", "AppliedDate", "Status"]
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        row = self._data[index.row()]
        col = self.headers[index.column()]
        val = row.get(col, "")
        if role == Qt.DisplayRole:
            return str(val)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return QVariant()

    def refresh(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


# ---------- Dialog Tambah/Edit ----------
class AddEditDialog(QDialog):
    def __init__(self, parent, options, data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Catatan" if data is None else "Edit Catatan")
        self.resize(420, 400)
        icon_path = Path(__file__).parent / "assets" / "favicon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.options = options
        self.data = data
        self._build_ui()
        if data:
            self._load_data()

    def _build_ui(self):
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.company = QLineEdit()
        self.position = QLineEdit()
        self.job_type = QComboBox()
        self.job_type.addItems(self.options["job_types"])
        self.platform = QComboBox()
        self.platform.addItems(self.options["platforms"])
        self.salary = QLineEdit()
        self.salary.setPlaceholderText("Contoh: 6.000.000 atau Negotiable")
        self.applied = QDateEdit()
        self.applied.setCalendarPopup(True)
        self.applied.setDate(QDate.currentDate())
        self.status = QComboBox()
        self.status.addItems(self.options["statuses"])

        layout.addRow("Nama Perusahaan:", self.company)
        layout.addRow("Posisi Dilamar:", self.position)
        layout.addRow("Tipe Pekerjaan:", self.job_type)
        layout.addRow("Platform:", self.platform)
        layout.addRow("Perkiraan Gaji:", self.salary)
        layout.addRow("Tanggal Melamar:", self.applied)
        layout.addRow("Status Loker:", self.status)

        btn_box = QHBoxLayout()
        btn_box.addWidget(QPushButton("💾 Simpan", clicked=self.accept))
        btn_box.addWidget(QPushButton("Batal", clicked=self.reject))
        layout.addRow(btn_box)
        self.setLayout(layout)

    def _load_data(self):
        d = self.data
        self.company.setText(d["Company"])
        self.position.setText(d["Position"])
        self.job_type.setCurrentText(d.get("Type", "Full Time"))
        self.salary.setText(d["Salary"])
        self.platform.setCurrentText(d["Platform"])
        self.status.setCurrentText(d["Status"])
        try:
            dt = datetime.strptime(d["AppliedDate"], "%Y-%m-%d")
            self.applied.setDate(QDate(dt.year, dt.month, dt.day))
        except Exception:
            self.applied.setDate(QDate.currentDate())

    def get_data(self):
        return {
            "Company": self.company.text().strip(),
            "Position": self.position.text().strip(),
            "Type": self.job_type.currentText(),
            "Platform": self.platform.currentText(),
            "Salary": self.salary.text().strip(),
            "AppliedDate": self.applied.date().toString("yyyy-MM-dd"),
            "Status": self.status.currentText()
        }


# ---------- Dialog Settings ----------
class SettingsDialog(QDialog):
    def __init__(self, parent, options):
        super().__init__(parent)
        self.setWindowTitle("Pengaturan Platform, Status & Tipe Pekerjaan")
        self.resize(500, 420)
        icon_path = Path(__file__).parent / "assets" / "favicon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.options = options
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout()

        def section(title, items, add_func, rm_func):
            box = QVBoxLayout()
            box.addWidget(QLabel(title))
            lst = QListWidget()
            lst.addItems(items)
            box.addWidget(lst)
            btn_add = QPushButton("＋ Tambah", clicked=lambda: add_func(lst))
            btn_rm = QPushButton("🗑️ Hapus", clicked=lambda: rm_func(lst))
            box.addWidget(btn_add)
            box.addWidget(btn_rm)
            return box, lst

        box1, self.list_platforms = section("Platform:", self.options["platforms"], self.add_item, self.remove_item)
        box2, self.list_statuses = section("Status:", self.options["statuses"], self.add_item, self.remove_item)
        box3, self.list_types = section("Tipe Pekerjaan:", self.options["job_types"], self.add_item, self.remove_item)

        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(QPushButton("💾 Simpan", clicked=self.on_save))
        btns.addWidget(QPushButton("Batal", clicked=self.reject))
        main = QVBoxLayout()
        main.addLayout(layout)
        main.addLayout(btns)
        self.setLayout(main)

    def add_item(self, list_widget):
        text, ok = QInputDialog.getText(self, "Tambah Item", "Masukkan nama:")
        if ok and text.strip():
            list_widget.addItem(text.strip())

    def remove_item(self, list_widget):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))

    def on_save(self):
        current_opts = load_pickle(OPTIONS_PATH, default=DEFAULT_OPTIONS.copy())
        current_opts.update({
            "platforms": [self.list_platforms.item(i).text() for i in range(self.list_platforms.count())],
            "statuses": [self.list_statuses.item(i).text() for i in range(self.list_statuses.count())],
            "job_types": [self.list_types.item(i).text() for i in range(self.list_types.count())],
        })
        save_pickle(current_opts, OPTIONS_PATH)
        QMessageBox.information(self, "Berhasil", "Pengaturan disimpan.")
        self.accept()


# ---------- Main Window ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jobseeker Notes")
        self.resize(1200, 680)
        icon_path = Path(__file__).parent / "assets" / "favicon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        init_db()
        self.options = load_options()
        self.data = fetch_all_jobs()
        self.filtered_data = self.data.copy()
        self._build_ui()
        self.setStyleSheet(APP_STYLE)
        self.header.setObjectName("header")

    def _build_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)

        # --- Header ---
        top = QHBoxLayout()
        self.header = QLabel("📋 Jobseeker Note System")
        self.header.setStyleSheet("font-size:18px; font-weight:700;")
        top.addWidget(self.header)

        top.addStretch()
        for txt, func in [
            ("＋ Tambah Catatan", self.on_add),
            ("⚙️ Pengaturan", self.on_settings),
            ("💾 Ekspor Excel", self.on_export)
        ]:
            b = QPushButton(txt)
            b.clicked.connect(func)
            top.addWidget(b)
        main.addLayout(top)

        # --- Filter ---
        filter_box = QHBoxLayout()
        self.filter_platform = QComboBox()
        self.filter_platform.addItem("🌐 Semua Platform")
        self.filter_platform.addItems(self.options["platforms"])
        self.filter_platform.currentIndexChanged.connect(self.apply_filter)

        self.filter_status = QComboBox()
        self.filter_status.addItem("📄 Semua Status")
        self.filter_status.addItems(self.options["statuses"])
        self.filter_status.currentIndexChanged.connect(self.apply_filter)

        self.filter_type = QComboBox()
        self.filter_type.addItem("💼 Semua Tipe")
        self.filter_type.addItems(self.options["job_types"])
        self.filter_type.currentIndexChanged.connect(self.apply_filter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari perusahaan atau posisi...")
        self.search_input.textChanged.connect(self.apply_filter)

        for w in [self.filter_platform, self.filter_status, self.filter_type, self.search_input]:
            filter_box.addWidget(w)
        main.addLayout(filter_box)

        # --- Table ---
        self.table = QTableView()
        self.model = SQLiteTableModel(self.filtered_data)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        main.addWidget(self.table)

        # --- Buttons bawah ---
        bottom = QHBoxLayout()
        bottom.addWidget(QPushButton("✏️ Edit", clicked=self.on_edit))
        bottom.addWidget(QPushButton("🗑️ Hapus", clicked=self.on_delete))
        bottom.addStretch()
        self.footer_label = QLabel("Ayun - Version 3.2.0")
        self.footer_label.setStyleSheet("font-size:11px; color:#888888;")
        self.footer_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        bottom.addWidget(self.footer_label)
        main.addLayout(bottom)
        self.setLayout(main)

    def refresh_table(self):
        self.data = fetch_all_jobs()
        self.apply_filter()

    def apply_filter(self):
        plat = self.filter_platform.currentText().replace("🌐 ", "")
        stat = self.filter_status.currentText().replace("📄 ", "")
        typ = self.filter_type.currentText().replace("💼 ", "")
        query = self.search_input.text().lower()
        filtered = [
            d for d in self.data
            if (plat == "Semua Platform" or d["Platform"] == plat)
            and (stat == "Semua Status" or d["Status"] == stat)
            and (typ == "Semua Tipe" or d.get("Type", "Full Time") == typ)
            and (query in d["Company"].lower() or query in d["Position"].lower())
        ]
        self.filtered_data = filtered
        self.model.refresh(self.filtered_data)

    def _selected_row(self):
        sel = self.table.selectionModel().selectedRows()
        return sel[0].row() if sel else None

    def on_add(self):
        dlg = AddEditDialog(self, self.options)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO job_notes (Company, Position, Platform, Salary, AppliedDate, Status, Type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data["Company"], data["Position"], data["Platform"],
                  data["Salary"], data["AppliedDate"], data["Status"], data["Type"]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Berhasil", "Catatan disimpan.")
            self.refresh_table()

    def on_edit(self):
        idx = self._selected_row()
        if idx is None:
            QMessageBox.warning(self, "Pilih", "Pilih baris untuk diedit.")
            return
        data = self.filtered_data[idx]
        dlg = AddEditDialog(self, self.options, data=data)
        if dlg.exec_() == QDialog.Accepted:
            new_data = dlg.get_data()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE job_notes SET Company=?, Position=?, Platform=?, Salary=?, AppliedDate=?, Status=?, Type=? WHERE ID=?
            """, (new_data["Company"], new_data["Position"], new_data["Platform"],
                  new_data["Salary"], new_data["AppliedDate"], new_data["Status"],
                  new_data["Type"], data["ID"]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Berhasil", "Data diperbarui.")
            self.refresh_table()

    def on_delete(self):
        idx = self._selected_row()
        if idx is None:
            QMessageBox.warning(self, "Pilih", "Pilih baris untuk dihapus.")
            return
        row = self.filtered_data[idx]
        confirm = QMessageBox.question(
            self, "Konfirmasi", f"Hapus {row['Company']} ({row['Position']})?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM job_notes WHERE ID=?", (row["ID"],))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Dihapus", "Catatan berhasil dihapus.")
            self.refresh_table()

    def on_settings(self):
        dlg = SettingsDialog(self, self.options)
        if dlg.exec_() == QDialog.Accepted:
            self.options = load_options()
            current_platform = self.filter_platform.currentText().replace("🌐 ", "")
            current_status = self.filter_status.currentText().replace("📄 ", "")
            current_type = self.filter_type.currentText().replace("💼 ", "")

            mapping = [
                (self.filter_platform, "platforms", "🌐", "Platform"),
                (self.filter_status, "statuses", "📄", "Status"),
                (self.filter_type, "job_types", "💼", "Tipe"),
            ]
            for combo, key, icon, label in mapping:
                combo.blockSignals(True)
                combo.clear()
                combo.addItem(f"{icon} Semua {label}")
                combo.addItems(self.options[key])
                combo.blockSignals(False)

            if current_platform in self.options["platforms"]:
                self.filter_platform.setCurrentText(current_platform)
            else:
                self.filter_platform.setCurrentIndex(0)

            if current_status in self.options["statuses"]:
                self.filter_status.setCurrentText(current_status)
            else:
                self.filter_status.setCurrentIndex(0)

            if current_type in self.options["job_types"]:
                self.filter_type.setCurrentText(current_type)
            else:
                self.filter_type.setCurrentIndex(0)

            self.refresh_table()
            QMessageBox.information(self, "Berhasil", "Pengaturan Telah Berhasil Dirubah.")

    def on_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Excel", str(Path.home() / "job_notes.xlsx"), "Excel Files (*.xlsx)"
        )
        if not path:
            return
        headers = ["No", "Company", "Position", "Type", "Platform", "Salary", "AppliedDate", "Status"]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Job Notes"
        ws.append(headers)
        for i, row in enumerate(self.filtered_data, 1):
            ws.append([
                i, row.get("Company", ""), row.get("Position", ""), row.get("Type", ""),
                row.get("Platform", ""), row.get("Salary", ""), row.get("AppliedDate", ""), row.get("Status", "")
            ])
        wb.save(path)
        QMessageBox.information(self, "Berhasil", f"Data disimpan ke {path}")


# ---------- Main ----------
def main():
    app = QApplication(sys.argv)
    icon_path = Path(__file__).parent / "assets" / "favicon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()