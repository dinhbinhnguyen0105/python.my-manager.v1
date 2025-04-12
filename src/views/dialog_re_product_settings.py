# src/views/dialog_re_product_settings.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableView

from src.ui.dialog_re_product_settings_ui import Ui_Dialog_REProductSettings
from src.controllers.re_controller import RESettingController, REImageDirController
from src import constants


class DialogREProductSetting(QDialog, Ui_Dialog_REProductSettings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("real estate product setting".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.controller = None
        self.current_table = None

        self.basic_setting_container.setHidden(True)
        self.image_dir_setting_container.setHidden(True)

        self.table_settings = [
            constants.RE_SETTING_STATUSES_TABLE,
            constants.RE_SETTING_CATEGORIES_TABLE,
            constants.RE_SETTING_DISTRICTS_TABLE,
            constants.RE_SETTING_OPTIONS_TABLE,
            constants.RE_SETTING_PROVINCES_TABLE,
            constants.RE_SETTING_WARDS_TABLE,
            constants.RE_SETTING_BUILDING_LINE_S_TABLE,
            constants.RE_SETTING_LEGAL_S_TABLE,
            constants.RE_SETTING_FURNITURE_S_TABLE,
        ]

        self.tableView.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows)

        self.set_events()

    def set_events(self):
        self.image_dir_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_IMG_DIR_TABLE)
        )
        self.statuses_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_STATUSES_TABLE)
        )
        self.categories_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_CATEGORIES_TABLE))
        self.districts_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_DISTRICTS_TABLE))
        self.options_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_OPTIONS_TABLE))
        self.provinces_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_PROVINCES_TABLE))
        self.wards_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_WARDS_TABLE))
        self.building_line_s_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_BUILDING_LINE_S_TABLE))
        self.legal_s_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_LEGAL_S_TABLE))
        self.furniture_s_radio.clicked.connect(
            lambda: self.set_model_and_ui(constants.RE_SETTING_FURNITURE_S_TABLE))

        self.delete_btn.clicked.connect(self.handle_delete)
        self.create_btn.clicked.connect(self.handle_create)
        self.create_btn_2.clicked.connect(self.handle_create)

    def set_model_and_ui(self, table_name):
        if table_name == constants.RE_SETTING_IMG_DIR_TABLE:
            self.controller = REImageDirController(table_name)
            self.current_table = table_name
            if not self.controller:
                return False
            self.tableView.setModel(self.controller.model)
            self.image_dir_setting_container.setHidden(False)
            self.basic_setting_container.setHidden(True)
            return True
        else:
            self.controller = RESettingController(table_name)
            self.current_table = table_name
            if not self.controller:
                return False
            self.tableView.setModel(self.controller.model)
            self.image_dir_setting_container.setHidden(True)
            self.basic_setting_container.setHidden(False)
            return True

    def handle_delete(self):
        if not self.controller:
            return False
        record_ids = self.get_selected_ids()
        if record_ids:
            reply = QMessageBox.question(
                self,
                "Confirm",
                f"Delete record(s) with ID(s): {record_ids}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.Yes:
                for record_id in record_ids:
                    self.controller.delete(record_id)
        else:
            QMessageBox.warning(
                self, "Warning", "Please select a row to delete.")

    def handle_create(self):
        if not self.controller or not self.current_table:
            return
        if self.current_table == constants.RE_SETTING_IMG_DIR_TABLE:
            self.controller.create_new({
                "value": self.image_dir_value_input.text(),
                "is_selected": 1 if self.img_dir_is_selected_checkbox.isChecked() else 0
            })
        else:
            self.controller.create_new({
                "label_vi": self.name_vi_input.text(),
                "label_en": self.name_en_input.text(),
                "value": self.value_input.text(),
            })

    def get_selected_ids(self):
        selection_model = self.tableView.selectionModel()
        selected_rows = selection_model.selectedRows()
        record_ids = []
        for selected_row in selected_rows:
            row = selected_row.row()
            id_column = self.controller.model.fieldIndex("id")
            if id_column != -1:
                index = self.controller.model.index(row, id_column)
                record_ids.append(self.controller.model.data(index))
        return record_ids
