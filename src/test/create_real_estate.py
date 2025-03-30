# src/test/create_real_estate.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6.QtCore import Qt
from src.ui.dialog_create_real_estate import Ui_DialogCreateRealEstate


# src/views/create_real_estate_dialgo.py
class CreateRealEstateDialog(QDialog, Ui_DialogCreateRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.sell__container.setVisible(False)
        # self.options__sell.toggled.connect(self.update_options_ui)
        # self.options__rent.toggled.connect(self.update_options_ui)
        # self.options__assignment.toggled.connect(self.update_options_ui)

    def update_options_ui(self):
        if self.options__sell.isChecked():
            self._setup_sell_ui()
        elif self.options__rent.isChecked():
            self._setup_rent_ui()
        elif self.options__assignment.isChecked():
            self._setup_assignment_ui()

    def _setup_sell_ui(self):
        self.sell__container.setVisible(True)
        pass

    def _setup_rent_ui(self):
        self.sell__container.setVisible(True)
        pass

    def _setup_assignment_ui(self):
        self.sell__container.setVisible(True)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_re_dialog = CreateRealEstateDialog()
    create_re_dialog.show()
    sys.exit(app.exec())
