# src/controllers/user_controller.py
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QDataWidgetMapper

from src.services.user_service import UserService, UserDataDirService, UserProxyService


class UserController(QObject):
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
        self.model.select()

    def load_data(self):
        self.model.select()
        self.mapper.setCurrentIndex(0)

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

    def submit_changes(self):
        if self.mapper.submit():
            if self.model.submitAll():
                QMessageBox.information(
                    None, "Success", "changes saved.".capitalize())
                return True
            else:
                QMessageBox.critical(
                    None, "Error", f"Database error: {self.model.lastError().text()}".capitalize(
                    )
                )
                return False
        else:
            QMessageBox.warning(
                None, "Warning", "Could not submit changes from UI.")
            return False

    def create(self, payload):
        payload.setdefault("status", 1)
        print(payload)
        try:
            if UserService.create(payload):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "user added successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.critical(
                    None, "Error", "failed to create new user.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def read(self, condition):
        try:
            user = UserService.read(condition)
            if not user:
                QMessageBox.warning(
                    None, "Warning", "user not found.".capitalize())
            return user
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return None

    def read_all(self):
        try:
            return UserService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return []

    def update(self, record_id, payload):
        payload.setdefault("status", 1)
        try:

            if UserService.update(record_id, payload):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "user updated successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "failed to update user.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def delete(self, record_id):
        try:
            if UserService.delete(record_id):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "user deleted successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "failed to delete user.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def deletes(self, record_ids):
        try:
            if UserService.delete_multiple(record_ids):
                self.model.select()
                QMessageBox.information(
                    None, "Success", f"{len(record_ids)} users deleted successfully.".capitalize(
                    )
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete users.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False


class UserDataDirController(QObject):
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
        self.model.select()

    def load_data(self):
        self.model.select()
        self.mapper.setCurrentIndex(0)

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

    def submit_changes(self):
        if self.mapper.submit():
            if self.model.submitAll():
                QMessageBox.information(
                    None, "Success", "Data directory changes saved.".capitalize())
                return True
            else:
                QMessageBox.critical(
                    None,
                    "Error",
                    f"Database error: {self.model.lastError().text()}".capitalize(
                    )
                )
                return False
        else:
            QMessageBox.warning(
                None, "Warning", "Could not submit data directory changes from UI.")
            return False

    def create(self, payload):
        try:
            if UserDataDirService.create(payload):
                self.load_data()
                QMessageBox.information(
                    None, "Success", "Data directory added successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to add data directory.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def read(self, record_id):
        try:
            data_dir = UserDataDirService.read(record_id)
            if not data_dir:
                QMessageBox.warning(
                    None, "Warning", "Data directory not found.".capitalize())
            return data_dir
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return None

    def read_all(self):
        try:
            return UserDataDirService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return []

    def update(self, record_id, payload):
        try:
            if UserDataDirService.update(record_id, payload):
                self.load_data()
                QMessageBox.information(
                    None, "Success", "Data directory updated successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update data directory.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def delete(self, record_id):
        try:
            if UserDataDirService.delete(record_id):
                self.load_data()
                QMessageBox.information(
                    None, "Success", "Data directory deleted successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete data directory.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def deletes(self, record_ids):
        try:
            if UserDataDirService.delete_multiple(record_ids):
                self.load_data()
                QMessageBox.information(
                    None, "Success", f"{len(record_ids)} data directories deleted successfully.".capitalize(
                    )
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete data directories.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def get_selected_data_dir(self):
        try:
            return UserDataDirService.get_selected_data_dir()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return None

    def set_selected_data_dir(self, record_id):
        try:
            if UserDataDirService.set_selected_data_dir(record_id):
                self.load_data()
                QMessageBox.information(
                    None, "Success", "Selected data directory updated.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update selected data directory.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False


class UserProxyController(QObject):
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
        self.model.select()

    def load_data(self):
        self.model.select()
        self.mapper.setCurrentIndex(0)

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

    def submit_changes(self):
        if self.mapper.submit():
            if self.model.submitAll():
                QMessageBox.information(
                    None, "Success", "Proxy changes saved.".capitalize())
                return True
            else:
                QMessageBox.critical(
                    None, "Error", f"Database error: {self.model.lastError().text()}".capitalize(
                    )
                )
                return False
        else:
            QMessageBox.warning(
                None, "Warning", "Could not submit proxy changes from UI.")
            return False

    def create(self, payload):
        try:
            if UserProxyService.create(payload):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Proxy added successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to add proxy.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def read(self, record_id):
        try:
            proxy = UserProxyService.read(record_id)
            if not proxy:
                QMessageBox.warning(
                    None, "Warning", "Proxy not found.".capitalize())
            return proxy
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return None

    def read_all(self):
        try:
            return UserProxyService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return []

    def update(self, record_id, payload):
        try:
            if UserProxyService.update(record_id, payload):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Proxy updated successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update proxy.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def delete(self, record_id):
        try:
            if UserProxyService.delete(record_id):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Proxy deleted successfully.".capitalize()
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete proxy.".capitalize()
                )
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False

    def deletes(self, record_ids):
        try:
            if UserProxyService.delete_multiple(record_ids):
                self.model.select()
                QMessageBox.information(
                    None, "Success", f"{len(record_ids)} proxies deleted successfully.".capitalize(
                    )
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete proxies.".capitalize())
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e).capitalize())
            return False
