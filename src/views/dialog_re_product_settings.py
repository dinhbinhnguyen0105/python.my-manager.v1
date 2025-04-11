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

        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.set_events()

    def set_events(self):
        self.statuses_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_STATUSES_TABLE)
        )
        self.categories_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_CATEGORIES_TABLE)
        )
        self.districts_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_DISTRICTS_TABLE)
        )
        self.options_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_OPTIONS_TABLE)
        )
        self.provinces_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_PROVINCES_TABLE)
        )
        self.wards_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_WARDS_TABLE)
        )
        self.building_line_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_BUILDING_LINE_S_TABLE)
        )
        self.legal_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_LEGAL_S_TABLE)
        )
        self.furniture_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_FURNITURE_S_TABLE)
        )

    def set_model(self, table_name):
        if table_name == constants.RE_SETTING_IMG_DIR_TABLE:
            self.controller = REImageDirController(table_name)
            self.current_table = table_name
            if not self.controller:
                return False
            self.tableView.setModel(self.controller.model)
            return True
        else:
            self.controller = RESettingController(table_name)
            self.current_table = table_name
            if not self.controller:
                return False
            self.tableView.setModel(self.controller.model)
            return True

    def handle_create(self):
        if not self.current_table or not self.controller:
            return False
        elif self.current_table in self.table_settings:
            data = {
                "label_vi": self.name_vi_input.text(),
                "label_en": self.name_en_input.text(),
                "value": self.value_input.text(),
            }
        elif self.current_table == constants.RE_SETTING_IMG_DIR_TABLE:
            data = {"value": self.ima}
        self.controller.create_new(data)
