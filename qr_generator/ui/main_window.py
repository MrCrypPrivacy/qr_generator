import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QFileDialog, QMenu, QDialog, QScrollArea, QGridLayout, QComboBox
)
from PyQt6.QtGui import QPixmap, QAction, QIcon
from PyQt6.QtCore import Qt
from logic.qr_generator import generate_qr_code
from ui.donate_window import DonateWindow

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APP_ICON_PATH = resource_path("assets/app_logo.png")
LOGOS_PATH = resource_path("assets/logos")
QR_SIZE = 300

class QRCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.wallet_address = ""
        self.qr_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.pixel_style = "square"
        self.selected_logo_path = None
        self.qr_pixmap = None
        self.current_qr_image = None

        self.setWindowTitle("QR Code Generator")
        self.setFixedSize(580, 700)
        if os.path.isfile(APP_ICON_PATH):
            self.setWindowIcon(QIcon(APP_ICON_PATH))

        self.init_ui()
        self.update_qr_preview()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.credit_label = QLabel("Created by 𝕄𝕣ℂ𝕣𝕪𝕡 ㉿")
        self.credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credit_label.setFixedHeight(30)
        self.layout.addWidget(self.credit_label)

        wallet_frame = QFrame()
        wallet_layout = QHBoxLayout(wallet_frame)

        self.wallet_entry = QLineEdit()
        self.wallet_entry.setPlaceholderText("Wallet Address or Text")
        self.wallet_entry.textChanged.connect(self.on_wallet_text_changed)
        self.wallet_entry.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.wallet_entry.customContextMenuRequested.connect(self.show_context_menu)

        wallet_layout.addWidget(self.wallet_entry)
        self.layout.addWidget(wallet_frame)

        logos_frame = QFrame()
        logos_layout = QHBoxLayout(logos_frame)

        self.btn_select_logo = QPushButton("Select Predefined Logo")
        self.btn_select_logo.clicked.connect(self.show_logo_selection)
        self.btn_upload_logo = QPushButton("Upload Your PNG Logo")
        self.btn_upload_logo.clicked.connect(self.upload_logo)
        self.btn_clear_logo = QPushButton("Remove Logo")
        self.btn_clear_logo.clicked.connect(self.clear_logo)

        logos_layout.addWidget(self.btn_select_logo)
        logos_layout.addWidget(self.btn_upload_logo)
        logos_layout.addWidget(self.btn_clear_logo)

        self.layout.addWidget(logos_frame)

        colors_frame = QFrame()
        colors_layout = QHBoxLayout(colors_frame)

        self.btn_color_fg = QPushButton("Select Pixel Color")
        self.btn_color_fg.clicked.connect(self.select_qr_color)

        self.btn_color_bg = QPushButton("Select Background Color")
        self.btn_color_bg.clicked.connect(self.select_bg_color)

        self.combo_style = QComboBox()
        self.combo_style.addItems(["square", "rounded", "dots"])
        self.combo_style.setCurrentText(self.pixel_style)
        self.combo_style.currentTextChanged.connect(self.on_style_changed)

        colors_layout.addWidget(self.btn_color_fg)
        colors_layout.addWidget(self.btn_color_bg)
        colors_layout.addWidget(self.combo_style)

        self.layout.addWidget(colors_frame)

        self.qr_label = QLabel()
        self.qr_label.setFixedSize(QR_SIZE, QR_SIZE)
        self.qr_label.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.qr_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_save_qr = QPushButton("Download QR Code")
        self.btn_save_qr.clicked.connect(self.save_qr)
        self.layout.addWidget(self.btn_save_qr)

        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)

        self.btn_github = QPushButton("GitHub")
        self.btn_github.clicked.connect(lambda: self.open_url("https://github.com/MrCrypPrivacy"))
        self.btn_twitter = QPushButton("𝕏")
        self.btn_twitter.clicked.connect(lambda: self.open_url("https://x.com/MrCrypPrivacy"))
        self.btn_donate = QPushButton("Donate")
        self.btn_donate.clicked.connect(self.open_donate)

        bottom_layout.addWidget(self.btn_github)
        bottom_layout.addWidget(self.btn_twitter)
        bottom_layout.addWidget(self.btn_donate)

        self.layout.addWidget(bottom_frame)

    def on_wallet_text_changed(self, text):
        self.wallet_address = text
        self.update_qr_preview()

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction(QAction("Copy", self, triggered=self.wallet_entry.copy))
        menu.addAction(QAction("Paste", self, triggered=self.wallet_entry.paste))
        menu.addAction(QAction("Cut", self, triggered=self.wallet_entry.cut))
        menu.addAction(QAction("Select All", self, triggered=self.wallet_entry.selectAll))
        menu.exec(self.wallet_entry.mapToGlobal(pos))

    def show_logo_selection(self):
        logos = []
        if os.path.isdir(LOGOS_PATH):
            for file in os.listdir(LOGOS_PATH):
                if file.lower().endswith(".png"):
                    logos.append(os.path.join(LOGOS_PATH, file))
        if not logos:
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Select Logo")
        dlg.setFixedSize(420, 240)

        scroll = QScrollArea(dlg)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        grid_layout = QGridLayout(scroll_content)

        for index, path in enumerate(logos):
            pixmap = QPixmap(path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            btn = QPushButton()
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.setFixedSize(80, 80)
            btn.clicked.connect(lambda _, p=path: self.select_logo_and_close(p, dlg))
            row, col = divmod(index, 4)
            grid_layout.addWidget(btn, row, col)

        scroll_content.setLayout(grid_layout)
        scroll.setWidget(scroll_content)

        layout = QVBoxLayout(dlg)
        layout.addWidget(scroll)
        dlg.setLayout(layout)

        dlg.exec()

    def select_logo_and_close(self, path, dialog):
        if os.path.isfile(path):
            self.selected_logo_path = path
            self.update_qr_preview()
        dialog.accept()

    def upload_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PNG Logo", filter="PNG Files (*.png)")
        if path and os.path.isfile(path):
            self.selected_logo_path = path
            self.update_qr_preview()

    def clear_logo(self):
        self.selected_logo_path = None
        self.update_qr_preview()

    def select_qr_color(self):
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.qr_color = color.name()
            self.update_qr_preview()

    def select_bg_color(self):
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color.name()
            self.update_qr_preview()

    def on_style_changed(self, style):
        self.pixel_style = style
        self.update_qr_preview()

    def update_qr_preview(self):
        if not self.wallet_address.strip():
            self.qr_label.clear()
            self.qr_pixmap = None
            self.current_qr_image = None
            return
        try:
            img = generate_qr_code(
                self.wallet_address,
                qr_color=self.qr_color,
                bg_color=self.bg_color,
                logo_path=self.selected_logo_path,
                size=1200,
                style=self.pixel_style
            )
            if img is None:
                self.qr_label.clear()
                self.qr_pixmap = None
                self.current_qr_image = None
                return

            self.current_qr_image = img

            pixmap = self.pil2pixmap(img)
            self.qr_pixmap = pixmap.scaled(QR_SIZE, QR_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.qr_label.setPixmap(self.qr_pixmap)
        except Exception as e:
            print("Error generating QR:", e)
            self.qr_label.setText("QR not found")
            self.qr_pixmap = None
            self.current_qr_image = None

    def pil2pixmap(self, img):
        from PyQt6.QtGui import QImage
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        qimg = QImage(data, img.width, img.height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(qimg)

    def save_qr(self):
        if not self.current_qr_image:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", filter="PNG Files (*.png)")
        if path:
            self.current_qr_image.save(path, format="PNG")

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def open_donate(self):
        dlg = DonateWindow(self)
        dlg.exec()
