# src/views/dialog_create_update_real_estate.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from src.ui.dialog_real_estate_ui import Ui_DialogRealEstate
from src.configs.real_estate_product import RealEstateProductConfigs
from src.controllers.real_estate_controller import RealEstateController


class DialogCreateUpdateRealEstate(QDialog, Ui_DialogRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fields = {
            "id": 0,
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
        self.setWindowTitle("Create Real Estate")

        self._setupImageDrop()

        self.option_assignment_w.clicked.connect(
            lambda: self.initialize_ui("assignment")
        )
        self.option_assignment_w.clicked.connect(
            lambda: self.set_field("option", "assignment")
        )
        self.option_sell_w.clicked.connect(lambda: self.initialize_ui("sell"))
        self.option_sell_w.clicked.connect(lambda: self.set_field("option", "sell"))
        self.option_rent_w.clicked.connect(lambda: self.initialize_ui("rent"))
        self.option_rent_w.clicked.connect(lambda: self.set_field("option", "rent"))

        self.pid_input.textChanged.connect(
            lambda: self.set_field("pid", self.pid_input.text())
        )
        self.categories_input.currentIndexChanged.connect(
            lambda: self.set_field("category", self.categories_input.currentData())
        )
        self.provinces_input.currentIndexChanged.connect(
            lambda: self.set_field("province", self.provinces_input.currentData())
        )
        self.districts_input.currentIndexChanged.connect(
            lambda: self.set_field("district", self.districts_input.currentData())
        )
        self.building_line_s_input.currentIndexChanged.connect(
            lambda: self.set_field(
                "building_line", self.building_line_s_input.currentData()
            )
        )
        self.furniture_s_input.currentIndexChanged.connect(
            lambda: self.set_field("furniture", self.furniture_s_input.currentData())
        )
        self.legal_s_input.currentIndexChanged.connect(
            lambda: self.set_field("legal", self.legal_s_input.currentData())
        )
        self.street_input.textChanged.connect(
            lambda: self.set_field("street", self.street_input.text())
        )
        self.area_input.textChanged.connect(
            lambda: self.set_field("area", self.area_input.text())
        )
        self.price_input.textChanged.connect(
            lambda: self.set_field("price", self.price_input.text())
        )
        self.function_input.textChanged.connect(
            lambda: self.set_field("function", self.function_input.text())
        )
        self.structure_input.textChanged.connect(
            lambda: self.set_field("structure", self.structure_input.text())
        )
        self.description_input.textChanged.connect(
            lambda: self.set_field("description", self.description_input.toPlainText())
        )

        self.buttonBox.accepted.disconnect()
        self.btn_save = self.buttonBox.button(QDialogButtonBox.StandardButton.Save)
        self.btn_save.clicked.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

    def get_fields(self):
        return self.fields

    def load_fields(self, fields):
        self.fields["id"] = fields.get("id")
        self.initialize_ui(fields.get("option"))
        if fields.get("option") == "assignment":
            self.option_assignment_w.setChecked(True)
            self.legal_s_input.setDisabled(True)
        elif fields.get("option") == "sell":
            self.option_sell_w.setChecked(True)
            self.legal_s_input.setDisabled(False)
        elif fields.get("option") == "rent":
            self.option_rent_w.setChecked(True)
            self.legal_s_input.setDisabled(True)

        self.fields["option"] = fields.get("option")

        self.pid_input.setText(fields.get("pid"))
        for i in range(self.categories_input.count()):
            if self.categories_input.itemData(i) == fields.get("category"):
                self.categories_input.setCurrentIndex(i)
                break
        for i in range(self.provinces_input.count()):
            if self.provinces_input.itemData(i) == fields.get("province"):
                self.provinces_input.setCurrentIndex(i)
                break
        for i in range(self.districts_input.count()):
            if self.districts_input.itemData(i) == fields.get("district"):
                self.districts_input.setCurrentIndex(i)
                break
        for i in range(self.building_line_s_input.count()):
            if self.building_line_s_input.itemData(i) == fields.get("building_line"):
                self.building_line_s_input.setCurrentIndex(i)
                break
        for i in range(self.furniture_s_input.count()):
            if self.furniture_s_input.itemData(i) == fields.get("furniture"):
                self.furniture_s_input.setCurrentIndex(i)
                break
        for i in range(self.legal_s_input.count()):
            if self.legal_s_input.itemData(i) == fields.get("legal"):
                self.legal_s_input.setCurrentIndex(i)
                break
        self.street_input.setText(fields.get("street"))
        self.area_input.setText(str(fields.get("area")))
        self.price_input.setText(str(fields.get("price")))
        self.function_input.setText(fields.get("function"))
        self.structure_input.setText(str(fields.get("structure")))
        self.description_input.setPlainText(fields.get("description"))
        image_paths = RealEstateController.get_image_path(fields.get("id"))
        self.fields["image_path"] = image_paths
        if not image_paths:
            self.image_input.setText("No image")
        else:
            self.image_input.setPixmap(
                QPixmap(image_paths[0]).scaled(
                    self.image_input.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def set_field(self, field, value):
        if not value:
            return
        value = value.strip()
        if not field == "description":
            value = value.lower()
        self.fields[field] = value

    def on_reject(self):
        pass

    def on_accept(self):
        if self.validate_fields():
            super().accept()
        else:
            return False

    def initialize_ui(self, option):
        if not self.fields.get("pid"):
            self.pid_input.setText(RealEstateController.generate_pid(option))

        configs = RealEstateProductConfigs()
        # category
        self.categories_input.clear()
        for category in configs.categories():
            self.categories_input.addItem(
                category.get("name")[0].capitalize(), category["value"]
            )
        # province
        self.provinces_input.clear()
        for province in configs.provinces():
            self.provinces_input.addItem(
                province.get("name")[0].capitalize(), province["value"]
            )

        # district
        self.districts_input.clear()
        for district in configs.districts():
            self.districts_input.addItem(
                district.get("name")[0].capitalize(), district["value"]
            )
        # ward
        self.wards_input.clear()
        for ward in configs.wards():
            self.wards_input.addItem(ward.get("name")[0].capitalize(), ward["value"])
        # building_line
        self.building_line_s_input.clear()
        for building_line in configs.building_line_s():
            self.building_line_s_input.addItem(
                building_line.get("name")[0].capitalize(), building_line["value"]
            )
        # legal
        self.legal_s_input.clear()
        for legal in configs.legal_s():
            self.legal_s_input.addItem(
                legal.get("name")[0].capitalize(), legal["value"]
            )
        # furniture
        self.furniture_s_input.clear()
        for furniture in configs.furniture_s():
            self.furniture_s_input.addItem(
                furniture.get("name")[0].capitalize(), furniture["value"]
            )

        if option == "assignment" or option == "rent":
            self.legal_s_input.setDisabled(True)
        else:
            self.legal_s_input.setDisabled(False)
        self.provinces_input.setDisabled(True)
        self.districts_input.setDisabled(True)

    def validate_fields(self):
        if len(self.fields.get("image_path")) < 1:
            QMessageBox.critical(None, "Error", "Please select at least one image.")
            return False
        if not self.fields.get("option"):
            QMessageBox.critical(None, "Error", "Please select a option.")
            return False
        if not self.fields.get("street"):
            QMessageBox.critical(None, "Error", "Street cannot be empty.")
            return False
        if (
            not self.fields.get("area")
            or self._str_to_float(self.fields.get("area")) == False
        ):
            QMessageBox.critical(None, "Error", "Area must be a number.")
            return False
        if (
            not self.fields.get("price")
            or self._str_to_float(self.fields.get("price")) == False
        ):
            QMessageBox.critical(None, "Error", "Price must be a number.")
            return False
        if (
            not self.fields.get("structure")
            or self._str_to_float(self.fields.get("structure")) == False
        ):
            QMessageBox.critical(None, "Error", "Structure cannot be empty.")
            return False
        if not self.fields.get("function"):
            QMessageBox.critical(None, "Error", "Function cannot be empty.")
            return False
        if not self.fields.get("description"):
            QMessageBox.critical(None, "Error", "Description cannot be empty.")
            return False
        return True

    def _str_to_float(self, str: str):
        try:
            _result = float(str)
            if _result == 0:
                return True
            return float(str)
        except ValueError:
            return False

    def _setupImageDrop(self):
        self.image_input.setAcceptDrops(True)
        self.image_input.dragEnterEvent = self._imagesDragEnterEvent
        self.image_input.dropEvent = self._imagesDropEvent

    def _imagesDragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _imagesDropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            images = [url.toLocalFile() for url in event.mimeData().urls()]
            self._handleDroppedImages(images)
            self.fields["image_path"] = images

    def _handleDroppedImages(self, image_paths):
        if image_paths:
            pixmap = QPixmap(image_paths[0])
            if not pixmap.isNull():
                self.image_input.setPixmap(
                    pixmap.scaled(
                        self.image_input.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                self.image_input.setText("Failed to load image.")
        else:
            self.image_input.setText("No images dropped.")
