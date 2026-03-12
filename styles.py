APP_STYLE = """
/* -------------------------------
   Global Style
--------------------------------*/
QWidget {
    font-family: "Segoe UI", Roboto, Arial;
    font-size: 14px;
    background: #f4f6fa;
    color: #222;
}

/* -------------------------------
   Header
--------------------------------*/
#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2575fc, stop:1 #6a11cb);
    color: white;
    padding: 18px 20px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* -------------------------------
   Buttons
--------------------------------*/
QPushButton {
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    background: #2575fc;
    color: white;
    font-size: 13px;
    font-weight: 600;
}
QPushButton:hover {
    background: #1e63d1;
}
QPushButton:pressed {
    background: #184fa3;
}
QPushButton#danger {
    background: #e53e3e;
}
QPushButton#danger:hover {
    background: #c53030;
}
QPushButton#ghost {
    background: transparent;
    color: #2575fc;
    border: 1px solid rgba(37,117,252,0.2);
}
QPushButton#ghost:hover {
    background: rgba(37,117,252,0.08);
}

/* -------------------------------
   Table View
--------------------------------*/
QTableView {
    background: white;
    border-radius: 10px;
    border: 1px solid #e1e8f5;
    gridline-color: #edf1f8;
    selection-background-color: #dceeff;
    selection-color: #111;
    font-size: 13px;
    alternate-background-color: #f9fbfe;
}
QHeaderView::section {
    background: #f0f4fa;
    padding: 10px;
    border: none;
    font-weight: 600;
    font-size: 13px;
}
QTableCornerButton::section {
    background: #f0f4fa;
    border: none;
}

/* -------------------------------
   Input Fields
--------------------------------*/
QLineEdit, QComboBox, QDateEdit {
    padding: 8px 10px;
    border: 1px solid #cfd9e7;
    border-radius: 8px;
    background: white;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #2575fc;
    background: #ffffff;
}

/* -------------------------------
   Labels
--------------------------------*/
QLabel {
    font-size: 13px;
}
QLabel#muted {
    color: #6b7280;
    font-size: 12px;
}

/* -------------------------------
   Dialog
--------------------------------*/
QDialog {
    background: #f7f9fc;
    border-radius: 12px;
    padding: 20px;
}
"""
