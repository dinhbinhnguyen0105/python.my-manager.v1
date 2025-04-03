from PyQt6.QtWidgets import QApplication
from src.views.dialog_create_real_estate import DialogCreateRealEstate
from src.models.real_estate_database import initialize_products_database

if __name__ == "__main__":
    app = QApplication([])
    initialize_products_database()
    dialog = DialogCreateRealEstate()
    dialog.show()
    app.exec()
