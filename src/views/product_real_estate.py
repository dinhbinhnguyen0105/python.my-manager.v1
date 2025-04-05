# src/views/product_real_estate.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QDialog, QWidget

from src.ui.product_real_estate_ui import Ui_ProductRealEstate
from src.models.real_estate_model import RealEstateProductModel
from src.controllers.real_estate_controller import RealEstateController


class ProductRealEstate(QWidget, Ui_ProductRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self.model = RealEstateProductModel()
        self.control = RealEstateController(self.model)

        self.setup_ui()

    def setup_ui(self):
        self.products_table.setModel(self.model)
        pass
