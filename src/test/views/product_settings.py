import sys
from PyQt6.QtWidgets import QApplication
from src.views.dialog_re_product_settings import DialogREProductSetting
from src.views.dialog_re_template_settings import DialogRETemplateSetting
from src.models.re_database import initialize_re_db

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("Failed to init db")
    dialog = DialogRETemplateSetting()
    dialog.show()
    sys.exit(app.exec())
