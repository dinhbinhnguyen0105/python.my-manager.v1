from PyQt6.QtWidgets import QApplication
from src.views.dialog_create_real_estate import DialogCreateRealEstate

if __name__ == "__main__":
    app = QApplication([])
    dialog = DialogCreateRealEstate()
    dialog.show()
    app.exec()
