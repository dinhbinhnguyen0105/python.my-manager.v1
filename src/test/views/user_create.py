import sys
from PyQt6.QtWidgets import QApplication
from src.views.dialog_user_create import DialogUserCreate
from src.models.user_database import initialize_user_db

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_user_db():
        print("Failed to init db")
    dialog = DialogUserCreate()
    dialog.show()
    sys.exit(app.exec())
