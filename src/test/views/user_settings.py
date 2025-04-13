import sys
from PyQt6.QtWidgets import QApplication
from src.views.dialog_user_settings import DialogUserSettings
from src.models.user_database import initialize_user_db

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_user_db():
        print("Failed to init db")
    dialog = DialogUserSettings()
    dialog.show()
    dialog.create_btn.clicked.connect(lambda: print(dialog.set_fields()))
    sys.exit(app.exec())
