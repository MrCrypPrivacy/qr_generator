import sys
import os
from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ASSETS_PATH = resource_path("assets")
DONATE_QR_PATH = resource_path("assets/donate_qr")

class DonateWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Donate")
        self.setFixedSize(620, 320)
        self.setWindowIcon(QIcon(os.path.join(ASSETS_PATH, "app_logo.png")))
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Panel Monero
        monero_frame = QVBoxLayout()
        monero_label = QLabel("Monero")
        monero_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monero_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.monero_wallet = QLineEdit("87k6ViTfSFGApzyyqr8jsuELYeBQ37yvndCWJcHgHDUf97LUz36JUutBtJiBYNBBDJeBCPN8gf6jW9f3HgJKeMsbUx3VsB5")
        self.monero_wallet.setReadOnly(True)
        self.monero_wallet.setFixedHeight(30)
        self.monero_wallet.setStyleSheet(
            "background-color: #2c2c2c; color: white; border-radius: 5px; padding-left: 5px;"
        )

        monero_qr_label = QLabel()
        monero_qr = QPixmap(os.path.join(DONATE_QR_PATH, "monero.png")).scaled(
            180, 180,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        monero_qr_label.setPixmap(monero_qr)
        monero_qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_copy_monero = QPushButton("Copy")
        btn_copy_monero.clicked.connect(lambda: self.copy_to_clipboard(self.monero_wallet.text()))

        monero_frame.addWidget(monero_label)
        monero_frame.addWidget(self.monero_wallet)
        monero_frame.addWidget(monero_qr_label)
        monero_frame.addWidget(btn_copy_monero)

        # Panel BTC Silent Payments
        btc_frame = QVBoxLayout()
        btc_label = QLabel("BTC Silent Payments")
        btc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btc_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.btc_wallet = QLineEdit("sp1qqg2s548t58g5x32jdhl33rxm8zy5r9aw3r7vrqfvrgjjz2c88dz96qc8qdge727xkd8umlwfr88gutqtu4dslrtkza0p6j0u44hwsgglmuky4xjj")
        self.btc_wallet.setReadOnly(True)
        self.btc_wallet.setFixedHeight(30)
        self.btc_wallet.setStyleSheet(
            "background-color: #2c2c2c; color: white; border-radius: 5px; padding-left: 5px;"
        )

        btc_qr_label = QLabel()
        btc_qr = QPixmap(os.path.join(DONATE_QR_PATH, "btc_sp.png")).scaled(
            180, 180,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        btc_qr_label.setPixmap(btc_qr)
        btc_qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_copy_btc = QPushButton("Copy")
        btn_copy_btc.clicked.connect(lambda: self.copy_to_clipboard(self.btc_wallet.text()))

        btc_frame.addWidget(btc_label)
        btc_frame.addWidget(self.btc_wallet)
        btc_frame.addWidget(btc_qr_label)
        btc_frame.addWidget(btn_copy_btc)

        layout.addLayout(monero_frame)
        layout.addLayout(btc_frame)

    def copy_to_clipboard(self, text: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
