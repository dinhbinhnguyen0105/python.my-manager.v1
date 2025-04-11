# src/controllers/re_controller.py
import uuid
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QDataWidgetMapper

# from .re_controller_utils import validate_new_product, get_image_path, get_columns
from src import constants
from src.controllers import re_controller_utils
from src.models.re_model import BaseSettingModel
from src.services.re_service import (
    REImageDirService,
    REProductService,
    RESettingService,
    RETemplateService,
)


class REProductController(QObject):
    current_record_changed = pyqtSignal(dict)

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.mapper = QDataWidgetMapper(self)
        self._initialize_mapper()

    def _initialize_mapper(self):
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(
            QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.currentIndexChanged.connect(self._on_current_index_changed)
        self.load_data()

    def bind_ui_widgets(self, **widgets_mapping):
        for field, widget in widgets_mapping.items():
            column = self.model.fieldIndex(field)
            if column != -1:
                self.mapper.addMapping(widget, column)

    def _on_current_index_changed(self, index):
        if index != -1:
            record = self.model.record(index)
            data = {}
            for i in range(record.count()):
                data[record.fieldName(i)] = record.value(i)
            self.current_record_changed.emit(data)

    def load_data(self):
        self.model.select()
        self.mapper.setCurrentIndex(0)  # Hiển thị bản ghi đầu tiên

    def submit_changes(self):
        if self.mapper.submit():
            if self.model.submitAll():
                QMessageBox.information(None, "Success", "Changes saved.")
                return True
            else:
                QMessageBox.critical(
                    None, "Error", f"Database error: {self.model.lastError().text()}"
                )
                return False
        else:
            QMessageBox.warning(
                None, "Warning", "Could not submit changes from UI.")
            return False

    def add_product(self, data):
        data.setdefault("image_paths", [])
        data.setdefault("area", 0.0)
        data.setdefault("structure", 0.0)
        data.setdefault("function", "")
        data.setdefault("street", "")
        data.setdefault("description", "")
        data.setdefault("price", 0.0)
        try:
            if not re_controller_utils.validate_new_product(data):
                return False
            if len(data.get("image_paths")) < 1:
                QMessageBox.critical(None, "Error", "Invalid images.")
                return False
            if REProductService.create(data):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product added successfully."
                )
                return True
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to create new real estate product."
                )
                return False

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def read_product(self, record_id):
        try:
            product = REProductService.read(record_id)
            if not product:
                QMessageBox.warning(None, "Warning", "Product not found.")
            return product
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return None

    def read_all_product(self):
        try:
            return REProductService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return []

    def update_product(self, record_id, data):
        data.setdefault("image_path", [])
        data.setdefault("area", 0.0)
        data.setdefault("structure", 0.0)
        data.setdefault("function", "")
        data.setdefault("description", "")
        data.setdefault("price", 0.0)
        try:
            if not re_controller_utils.validate_new_product(data):
                return False
            if REProductService.update(record_id, data):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product updated successfully."
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update product.")
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def delete_product(self, record_id):
        try:
            if REProductService.delete(record_id):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product deleted successfully."
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete product.")
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    @staticmethod
    def get_image_paths(record_id):
        return re_controller_utils.get_image_path(record_id)

    @staticmethod
    def get_columns():
        return re_controller_utils.get_columns()
