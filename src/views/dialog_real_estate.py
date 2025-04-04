from PyQt6.QtWidgets import QDialog, QApplication
from src.ui.dialog_real_estate_ui import Ui_DialogRealEstate


class DialogRealEstate(QDialog, Ui_DialogRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = DialogRealEstate()
    dialog.show()
    sys.exit(app.exec())
