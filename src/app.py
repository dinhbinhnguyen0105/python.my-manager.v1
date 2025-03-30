# src/app.py
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from src.models.database import initialize_database
from src.views.main_window import MainWindow


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        # Khởi tạo database
        if not self.initialize_app():
            sys.exit(1)

        # Tạo main window
        self.main_window = MainWindow()
        self.main_window.show()

    def initialize_app(self):
        """Khởi tạo các thành phần chính của ứng dụng"""
        try:
            if not initialize_database():
                QMessageBox.critical(
                    None,
                    "Database Error",
                    "Không thể kết nối database!"
                )
                return False
            return True
        except Exception as e:
            QMessageBox.critical(
                None,
                "Lỗi Khởi Tạo",
                f"Lỗi khi khởi tạo ứng dụng: {str(e)}"
            )
            return False
