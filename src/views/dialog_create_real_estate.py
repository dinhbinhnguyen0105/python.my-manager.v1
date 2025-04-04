# src/views/dialog_create_real_estate.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QDialogButtonBox, QMessageBox
from src.ui.dialog_create_real_estate_ui import Ui_DialogCreateRealEstate
from src.configs.real_estate_product import RealEstateProductConfigs
from src.controllers.real_estate_controller import RealEstateController
from src.models.real_estate_model import RealEstateProductModel


class DialogCreateRealEstate(QDialog, Ui_DialogCreateRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize QDialog
        self.fields = {
            "image_path": [],
            "option": "",
            "pid": "",
            "category": "",
            "province": "",
            "district": "",
            "ward": "",
            "street": "",
            "area": 0,
            "price": 0,
            "function": "",
            "structure": 0,
            "building_line": "",
            "furniture": "",
            "legal": "",
            "description": "",
            "status": 1,
        }
        self.setupUi(self)

        self.model = RealEstateProductModel()
        self.controller = RealEstateController(self.model)

        self.setWindowTitle("Create Real Estate")
        self.setFixedSize(self.size())

        self.legal.setDisabled(True)

        self.sell.clicked.connect(
            lambda: self._setupUi("sell"))
        self.rent.clicked.connect(
            lambda: self._setupUi("rent"))
        self.assignment.clicked.connect(
            lambda: self._setupUi("assignment"))

        self.category.currentIndexChanged.connect(lambda: self._setField(
            "category", self.category.currentData()))
        self.province.currentIndexChanged.connect(lambda: self._setField(
            "province", self.province.currentData()))
        self.district.currentIndexChanged.connect(lambda: self._setField(
            "district", self.district.currentData()))
        self.ward.currentIndexChanged.connect(lambda: self._setField(
            "ward", self.ward.currentData()))
        self.street.textChanged.connect(lambda: self._setField(
            "street", self.street.text()))
        self.area.textChanged.connect(lambda: self._setField(
            "area", self.area.text()))
        self.price.textChanged.connect(lambda: self._setField(
            "price", self.price.text()))
        self.function.textChanged.connect(lambda: self._setField(
            "function", self.function.text()))
        self.structure.textChanged.connect(lambda: self._setField(
            "structure", self.structure.text()))
        self.building_line.currentIndexChanged.connect(lambda: self._setField(
            "building_line", self.building_line.currentData()))
        self.furniture.currentIndexChanged.connect(lambda: self._setField(
            "furniture", self.furniture.currentData()))
        self.legal.currentIndexChanged.connect(lambda: self._setField(
            "legal", self.legal.currentData()))
        self.description.textChanged.connect(lambda: self._setField(
            "description", self.description.toPlainText()))

        self.btn_save = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Save)
        self.btn_save.disconnect()
        self.btn_save.clicked.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.setupImageDrop()

    def _setupUi(self, option):
        self.fields["option"] = option
        self.setupComboBox()
        if option == "rent" or option == "assignment":
            self.legal.setDisabled(True)
        else:
            self.legal.setDisabled(False)
        # Generate a unique PID

        self.fields["pid"] = self.controller.generate_pid(option)
        self.pid.setText(self.fields["pid"])

    def _setField(self, field, value):
        value = value.strip()
        if not field == "description":
            value = value.lower()
        self.fields[field] = value

    def setupComboBox(self):
        # Setup combo boxes with data from RealEstateProductConfigs
        configs = RealEstateProductConfigs()
        # category
        self.category.clear()
        for category in configs.categories():
            self.category.addItem(category.get(
                "name")[0].capitalize(), category["value"])
        # province
        self.province.clear()
        for province in configs.provinces():
            self.province.addItem(province.get(
                "name")[0].capitalize(), province["value"])

        # district
        self.district.clear()
        for district in configs.districts():
            self.district.addItem(district.get(
                "name")[0].capitalize(), district["value"])
        # ward
        self.ward.clear()
        for ward in configs.wards():
            self.ward.addItem(ward.get(
                "name")[0].capitalize(), ward["value"])
        # building_line
        self.building_line.clear()
        for building_line in configs.building_line_s():
            self.building_line.addItem(building_line.get(
                "name")[0].capitalize(), building_line["value"])
        # legal
        self.legal.clear()
        for legal in configs.legal_s():
            self.legal.addItem(legal.get(
                "name")[0].capitalize(), legal["value"])
        # furniture
        self.furniture.clear()
        for furniture in configs.furniture_s():
            self.furniture.addItem(furniture.get(
                "name")[0].capitalize(), furniture["value"])

    def on_accept(self):
        # Handle the accept button click
        if self.validate():
            print("Fields:", self.fields)
            self.controller.add_product(self.fields)
            self.accept()
        else:
            return False

    def on_reject(self):
        # Handle the reject button click
        pass

    def validate(self):
        if len(self.fields.get("image_path")) < 1:
            QMessageBox.critical(
                None, "Error", "Please select at least one image.")
            return False
        if not self.fields.get("street"):
            QMessageBox.critical(None, "Error", "Street cannot be empty.")
            return False
        if not self.fields.get("area") or self.str_to_float(self.fields.get("area")) == False:
            QMessageBox.critical(None, "Error", "Area must be a number.")
            return False
        if not self.fields.get("price") or self.str_to_float(self.fields.get("price")) == False:
            QMessageBox.critical(None, "Error", "Price must be a number.")
            return False
        if not self.fields.get("structure") or self.str_to_float(self.fields.get("structure")) == False:
            QMessageBox.critical(None, "Error", "Structure cannot be empty.")
            return False
        if not self.fields.get("function"):
            QMessageBox.critical(
                None, "Error", "Function cannot be empty.")
            return False
        if not self.fields.get("description"):
            QMessageBox.critical(
                None, "Error", "Description cannot be empty.")
            return False

        return True

    def str_to_float(self, str: str):
        try:
            _result = float(str)
            if _result == 0:
                return True
            return float(str)
        except ValueError:
            return False

    def setupImageDrop(self):
        # Configure self.images as a drag-and-drop widget
        self.images.setAcceptDrops(True)

        # Override dragEnterEvent and dropEvent for self.images
        self.images.dragEnterEvent = self.imagesDragEnterEvent
        self.images.dropEvent = self.imagesDropEvent

    def imagesDragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def imagesDropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            self.fields["image_path"] = [url.toLocalFile()
                                         for url in event.mimeData().urls()]
            self.handleDroppedImages(self.fields["image_path"])

    def handleDroppedImages(self, image_paths):
        if image_paths:
            pixmap = QPixmap(image_paths[0])
            if not pixmap.isNull():
                self.images.setPixmap(pixmap.scaled(
                    self.images.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                self.images.setText("Failed to load image.")
        else:
            self.images.setText("No images dropped.")
