import sys
from PyQt6.QtWidgets import QApplication
from src.views.dialog_re_product import DialogREProduct
from src.views.re_product import REProduct
from src.controllers.re_controller import REProductController
from src.models.re_database import initialize_re_db
from src.models.re_model import REProductModel


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("Failed to init db")
    window = REProduct()
    window.show()
    sys.exit(app.exec())
