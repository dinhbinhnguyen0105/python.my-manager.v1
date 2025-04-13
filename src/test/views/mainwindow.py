import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow

from src.models.re_database import initialize_re_db
from src.models.user_database import initialize_user_db

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("Failed to init db")
    if not initialize_user_db():
        print("Failed to init db")

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
