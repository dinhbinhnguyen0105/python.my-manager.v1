# src/controllers/real_estate_controller.py
import uuid
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

    def read_product(self, pid: str) -> RealEstateProductType:
        try:
            product = RealEstateProductService.read(pid)
            if not product:
                QMessageBox.warning(None, "Warning", "Product not found.")
            return product
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return None

    def read_all_product(self) -> list[RealEstateProductType]:
        try:
            return RealEstateProductService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return []

    def update_product(self, data: dict) -> bool:
        try:
            success = RealEstateProductService.update(data)
            if success:
                self.model.select()
                self.data_changed.emit()
                QMessageBox.information(
                    None, "Success", "Real estate product updated successfully.")
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update product.")
            return success
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def delete_product(self, pid: str) -> bool:
        try:
            success = RealEstateProductService.delete(pid)
            if success:
                self.model.select()
                self.data_changed.emit()
                QMessageBox.information(
                    None, "Success", "Real estate product deleted successfully.")
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete product.")
            return success
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    @staticmethod
    def generate_pid(option: str) -> str:
        try:
            while True:
                uuid_str = str(uuid.uuid4())
                pid = uuid_str.replace("-", "")[:8]
                if option.lower() == "sell":
                    pid = "S." + pid
                elif option.lower() == "rent":
                    pid = "R." + pid
                elif option.lower() == "assignment":
                    pid = "A." + pid
                else:
                    raise ValueError("Invalid option")
                pid = ("RE." + pid).lower()
                if not RealEstateProductService.check_unique_pid(pid):
                    return pid
                else:
                    continue
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            raise Exception("Failed to generate PID.")

    def _validate_new_product(self, data):
        configs = RealEstateProductConfigs()
        allowed_values = configs.allowed_values()

        if data.get("option") not in allowed_values["options"]:
            QMessageBox.critical(None, "Error", "Invalid option selected.")
            return False
        if data.get("category") not in allowed_values["categories"]:
            QMessageBox.critical(None, "Error", "Invalid category selected.")
            return False
        if data.get("province") not in allowed_values["provinces"]:
            QMessageBox.critical(None, "Error", "Invalid province selected.")
            return False
        if data.get("district") not in allowed_values["districts"]:
            QMessageBox.critical(None, "Error", "Invalid district selected.")
            return False
        if data.get("ward") not in allowed_values["wards"]:
            QMessageBox.critical(None, "Error", "Invalid ward selected.")
            return False
        if data.get("building_line") not in allowed_values["building_line_s"]:
            QMessageBox.critical(
                None, "Error", "Invalid building line selected.")
            return False
        if data.get("legal") not in allowed_values["legal_s"]:
            QMessageBox.critical(None, "Error", "Invalid legal selected.")
            return False
        if data.get("furniture") not in allowed_values["furniture_s"]:
            QMessageBox.critical(None, "Error", "Invalid furniture selected.")
            return False
        if data.get("price") <= 0:
            QMessageBox.critical(
                None, "Error", "Price must be greater than 0.")
            return False
        if data.get("area") <= 0:
            QMessageBox.critical(None, "Error", "Area must be greater than 0.")
            return False
        if data.get("structure") <= 0:
            QMessageBox.critical(
                None, "Error", "Structure must be greater than 0.")
            return False
        if not data.get("description"):
            QMessageBox.critical(None, "Error", "Description cannot be empty.")
            return False
        if not data.get("function"):
            QMessageBox.critical(None, "Error", "Function cannot be empty.")
            return False
        if not data.get("furniture"):
            QMessageBox.critical(None, "Error", "Furniture cannot be empty.")
            return False
        return True
