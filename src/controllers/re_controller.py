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

    def add_product(self, payload):
        payload.setdefault("image_paths", [])
        payload.setdefault("area", 0.0)
        payload.setdefault("structure", 0.0)
        payload.setdefault("function", "")
        payload.setdefault("street", "")
        payload.setdefault("description", "")
        payload.setdefault("price", 0.0)
        try:
            if not re_controller_utils.validate_new_product(payload):
                return False
            if len(payload.get("image_paths")) < 1:
                QMessageBox.critical(None, "Error", "Invalid images.")
                return False
            if REProductService.create(payload):
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

    def read_product(self, record_id, raw=False):
        try:
            if not raw:
                product = REProductService.read(record_id)
            else:
                product = REProductService.read_raw(record_id)
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

    def update_product(self, record_id, payload):
        payload.setdefault("image_path", [])
        payload.setdefault("area", 0.0)
        payload.setdefault("structure", 0.0)
        payload.setdefault("function", "")
        payload.setdefault("description", "")
        payload.setdefault("price", 0.0)
        try:
            if not re_controller_utils.validate_new_product(payload):
                return False
            if REProductService.update(record_id, payload):
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
        return RESettingService.get_columns()

    @staticmethod
    def generate_pid(option):
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
                if not REProductService.is_value_existed(
                    constants.RE_PRODUCT_TABLE, {"pid": pid}
                ):
                    return pid
                else:
                    continue
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            raise Exception("Failed to generate PID.")

    @staticmethod
    def validate_new_product(fields):
        if not fields.get("pid") or REProductService.is_value_existed(constants.RE_PRODUCT_TABLE, {"pid": fields.get("pid")}):
            QMessageBox.critical(None, "Error", "Invalid pid.")
            return False
        if (
            not isinstance(fields.get("area"), (int, float))
            or not isinstance(fields.get("structure"), (int, float))
            or not isinstance(fields.get("price"), (int, float))
        ):
            QMessageBox.critical(
                None, "Error", "Area, structure, and price must be numbers."
            )
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_STATUSES_TABLE, {
                "id": fields.get("status_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid status selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_PROVINCES_TABLE, {
                "id": fields.get("province_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid province selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_DISTRICTS_TABLE, {
                "id": fields.get("district_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid district selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_WARDS_TABLE, {"id": fields.get("ward_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid ward selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_OPTIONS_TABLE, {"id": fields.get("option_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid option selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_CATEGORIES_TABLE, {
                "id": fields.get("category_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid category selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_BUILDING_LINE_S_TABLE,
            {"id": fields.get("building_line_id")},
        ):
            QMessageBox.critical(
                None, "Error", "Invalid building_line selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_FURNITURE_S_TABLE,
            {"id": fields.get("furniture_id")},
        ):
            QMessageBox.critical(None, "Error", "Invalid furniture selected.")
            return False
        if not REProductService.is_value_existed(
            constants.RE_SETTING_LEGAL_S_TABLE, {"id": fields.get("legal_id")}
        ):
            QMessageBox.critical(None, "Error", "Invalid legal selected.")
            return False
        return True


class RESettingController(QObject):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.model = BaseSettingModel(self.table_name)

    def create_new(self, payload):
        try:
            if RESettingService.create(self.table_name, payload):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to create new record.")

            return True
        except Exception as e:
            error_msg = f"Error creating new record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def read(self, record_id):
        try:
            return RESettingService.read(self.table_name, record_id)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    def update(self, record_id: int, payload: dict):
        try:
            if RESettingService.update(self.table_name, record_id, payload):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to update record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error updating record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def delete(self, record_id: int):
        try:
            if RESettingService.delete(self.table_name, record_id):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to delete record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error deleting record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def read_all(self):
        try:
            return RESettingService.read_all(self.table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    @staticmethod
    def static_read_all(table_name):
        try:
            return RESettingService.read_all(table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    @staticmethod
    def static_read(table_name, id):
        try:
            return RESettingService.read(table_name, id)
        except Exception as e:
            error_msg = f"Error fetching record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []


class RETemplateController(QObject):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.model = BaseSettingModel(self.table_name)

    def create_new(self, payload):
        if not payload.get("value"):
            QMessageBox.critical(
                None, "Error", f"Input field cannot be empty.")
        try:
            tid = self.generate_tid()
            result = RETemplateService.create(
                self.table_name,
                {"tid": tid, "value": payload.get(
                    "value"), "option_id": payload.get("option_id")},
            )
            self.model.select()
            return result
        except Exception as e:
            error_msg = f"Error creating new record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def read(self, record_id):
        try:
            return RETemplateService.read(self.table_name, record_id)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    def update(self, record_id: int, payload: dict):
        try:
            if RETemplateService.update(self.table_name, record_id, payload):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to update record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error updating record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def delete(self, record_id: int):
        try:
            if RETemplateService.delete(self.table_name, record_id):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to delete record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error deleting record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def read_all(self):
        try:
            return RETemplateService.read_all(self.table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    def generate_tid(self):
        try:
            while True:
                uuid_str = str(uuid.uuid4())
                tid = uuid_str.replace("-", "")[:8]
                if self.table_name == constants.RE_TEMPLATE_TITLE_TABLE:
                    tid = "T.T." + tid
                elif self.table_name == constants.RE_TEMPLATE_DESCRIPTION_TABLE:
                    tid = "T.D." + tid
                if not RETemplateService.is_value_existed(self.table_name, {"tid": tid}):
                    return tid
                else:
                    continue
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            raise Exception("Failed to generate TID.")

    def get_ids_by_condition(self, condition):
        return RETemplateService.get_ids_by_condition(self.table_name, condition)


class REImageDirController(QObject):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.model = BaseSettingModel(self.table_name)

    def read(self, condition):
        try:
            return REImageDirService.read(condition)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    def read_all(self):
        try:
            return REImageDirService.read_all()
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    def create_new(self, payload):
        try:
            if REImageDirService.create(payload):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to create new record.")

            return True
        except Exception as e:
            error_msg = f"Error creating new record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def update(self, record_id, payload):
        try:
            if REImageDirService.update(record_id, payload):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to update record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error updating record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def delete(self, record_id):
        try:
            if REImageDirService.delete(record_id):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to delete record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error deleting record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
