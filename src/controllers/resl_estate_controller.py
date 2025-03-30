# src/controllers/resl_estate_controller.py
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QMessageBox, QDataWidgetMapper
from src.models.real_estate_model import RealEstateModel
from src.services.real_estate_service import RealEstateService


class RealEstateController(QObject):
    real_estate_data_update = pyqtSignal()

    def __init__(self, model: RealEstateModel):
        super().__init__()
        self.model = model
        self.mapper = QDataWidgetMapper()
        self._initialize_mapper()

    def _initialize_mapper(self):
        """ Cấu hình Data Mapper để liên kết UI với Model """
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.mapper.setOrientation(Qt.Orientation.Vertical)
        self.mapper.toFirst()

    def bind_ui_widgets(self, **widget_mappings):
        for widget, column in widget_mappings.items():
            self.mapper.addMapping(column, self.model.fieldIndex(widget))
        self.mapper.toFirst()

    def current_record_pid(self):
        """ Lấy PID của bản ghi hiện tại """
        return self.model.data(self.model.index(self.mapper.currentIndex(), 1))  # PID là cột thứ hai (index 1)

    def set_current_index(self, index):
        """ Đặt index hiện tại của mapper """
        self.mapper.setCurrentIndex(index)

    def add_real_estate(self, data):
        try:
            if RealEstateService.create_real_estate(data):
                self.model.select()
                self.real_estate_data_update.emit()
                QMessageBox.information(
                    None, "Successful", "Add real estate product!")
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to add real estate product.")
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def update_current_real_estate(self, data):
        pid = self.current_record_pid()
        if not pid:
            QMessageBox.warning(
                None, "Warning", "No record selected for update.")
            return

        try:
            if RealEstateService.update_real_estate(pid, data):
                self.model.select()
                self.real_estate_data_update.emit()
                QMessageBox.information(
                    None, "Successful", f"Updated real estate product with PID: {pid}")
            else:
                QMessageBox.warning(
                    None, "Warning", f"Failed to update real estate product with PID: {pid}")
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def delete_current_real_estate(self):
        pid = self.current_record_pid()
        if not pid:
            QMessageBox.warning(
                None, "Warning", "No record selected for deletion.")
            return

        reply = QMessageBox.question(
            None,
            "Confirm Delete",
            f"Are you sure you want to delete the real estate product with PID: {pid}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if RealEstateService.delete_real_estate(pid):
                    self.model.select()
                    self.real_estate_data_update.emit()
                    QMessageBox.information(
                        None, "Successful", f"Deleted real estate product with PID: {pid}")
                else:
                    QMessageBox.warning(
                        None, "Warning", f"Failed to delete real estate product with PID: {pid}")
            except Exception as e:
                QMessageBox.critical(None, "Error", str(e))

    def read_real_estate(self, pid):
        try:
            real_estate = RealEstateService.read_real_estate(pid)
            return real_estate
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return None

    def read_all_real_estates(self):
        try:
            real_estates = RealEstateService.read_all_real_estates()
            return real_estates
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return []
