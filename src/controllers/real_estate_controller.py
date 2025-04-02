from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QDataWidgetMapper
from src.models.real_estate_model import RealEstateProductModel
from src.services.real_estate_services import RealEstateProductService
from src.configs.real_estate_product import RealEstateProductConfigs
from src._types import RealEstateProductType


class RealEstateController(QObject):
    data_changed = pyqtSignal()

    def __init__(self, model: RealEstateProductModel):
        super().__init__()
        self.model = model
        self.mapper = QDataWidgetMapper()
        self._initialize_mapper()

    def _initialize_mapper(self):
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.mapper.setOrientation(Qt.Orientation.Vertical)
        self.mapper.toFirst()

    def add_product(self, data: RealEstateProductType):
        try:
            RealEstateProductService.create(data)
            self.model.select()
            self.data_changed.emit()
            QMessageBox.information(
                None, "Success", "Real estate product added successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def _validate_new_product(self, data):
        # Implement validation logic here
        # real_estate_product_configs = RealEstateProductConfigs()
        # if data.get("option") not in real_estate_product_configs.options():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid option selected.")
        #     return False
        # if data.get("category") not in real_estate_product_configs.categories():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid category selected.")
        #     return False
        # if data.get("province") not in real_estate_product_configs.provinces():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid province selected.")
        #     return False
        # if data.get("district") not in real_estate_product_configs.districts():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid district selected.")
        #     return False
        # if data.get("ward") not in real_estate_product_configs.wards():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid ward selected.")
        #     return False
        # if data.get("building_line") not in real_estate_product_configs.building_line_s():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid building line selected.")
        #     return False
        # if data.get("legal") not in real_estate_product_configs.legal_s():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid legal selected.")
        #     return False
        # if data.get("furniture") not in real_estate_product_configs.furniture_s():
        #     QMessageBox.critical(
        #         None, "Error", "Invalid furniture selected.")
        #     return False
        # if data.get("price") <= 0:
        #     QMessageBox.critical(
        #         None, "Error", "Price must be greater than 0.")
        #     return False
        # if data.get("area") <= 0:
        #     QMessageBox.critical(
        #         None, "Error", "Area must be greater than 0.")
        #     return False
        # if data.get("structure") <= 0:
        #     QMessageBox.critical(
        #         None, "Error", "Structure must be greater than 0.")
        #     return False
        # if not data.get("description"):
        #     QMessageBox.critical(
        #         None, "Error", "Description cannot be empty.")
        #     return False
        # if not data.get("function"):
        #     QMessageBox.critical(
        #         None, "Error", "Function cannot be empty.")
        #     return False
        # if not data.get("furniture"):
        #     QMessageBox.critical(
        #         None, "Error", "Furniture cannot be empty.")
        #     return False

        return True
