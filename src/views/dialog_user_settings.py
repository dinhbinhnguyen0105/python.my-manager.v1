# src/views/dialog_user_settings.py
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QMessageBox, QWidget, QMenu, QDialog
from PyQt6.QtGui import QAction

from src import constants
from src.ui.dialog_user_settings_ui import Ui_Dialog_UserSettings
from src.controllers.user_controller import UserDataDirController, UserProxyController
from src.models.user_model import UserDataDirModel, UserProxyModel


class DialogUserSettings(QDialog, Ui_Dialog_UserSettings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("user settings".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.current_table = None
        self.fields = None
        self.model = None
        self.controller = None

        self.proxy_container.setHidden(True)
        self.udd_container.setHidden(True)

        self.set_events()

    def set_events(self):
        self.udd_radio.clicked.connect(lambda: self.set_ui_and_model(
            constants.USER_SETTING_USER_DATA_DIR_TABLE))
        self.proxy_radio.clicked.connect(
            lambda: self.set_ui_and_model(constants.USER_SETTING_PROXY_TABLE))
        self.create_new_btn.clicked.connect(lambda: self.handle_create())

        self.buttonBox.rejected.connect(self.reject)

    def set_ui_and_model(self, table_name):
        if table_name == constants.USER_SETTING_PROXY_TABLE:
            self.proxy_container.setHidden(False)
            self.udd_container.setHidden(True)
            self.model = UserProxyModel()
            self.controller = UserProxyController(self.model)
        elif table_name == constants.USER_SETTING_USER_DATA_DIR_TABLE:
            self.proxy_container.setHidden(True)
            self.udd_container.setHidden(False)
            self.model = UserDataDirModel()
            self.controller = UserDataDirController(self.model)

        self.current_table = table_name
        self.fields = None

        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(
            self.table_view.SelectionBehavior.SelectRows
        )
        self.table_view.setSortingEnabled(True)

        self.table_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(
            self.show_context_menu)

        return True

    def show_context_menu(self, pos: QPoint):
        global_pos = self.table_view.mapToGlobal(pos)
        menu = QMenu(self.table_view)
        delete_action = QAction("Delete", self)

        delete_action.triggered.connect(self.handle_delete)

        menu.addAction(delete_action)

        menu.popup(global_pos)

    def get_fields(self):
        if self.current_table == constants.USER_SETTING_USER_DATA_DIR_TABLE:
            return {
                "value": self.udd_input.text(),
                "is_selected": 1 if self.udd_is_selected_checkbox.isChecked() else 0
            }
        elif self.current_table == constants.USER_SETTING_PROXY_TABLE:
            return {"value": self.proxy_input.text()}

    def handle_create(self):
        self.fields = self.get_fields()
        if not self.fields:
            return False
        if not self.controller.create(self.fields):
            return False
        return True

    def handle_delete(self):
        selected_ids = self.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(
                self, "Warning", "No (user_data_dir container)/ (proxy) selected.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete these (user_data_dir container)/ (proxy): {', '.join(map(str, selected_ids))}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.deletes(selected_ids)
        else:
            pass

    def get_selected_ids(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        rows = [selected_index.row() for selected_index in selected_indexes]
        return self.model.get_record_ids(rows)
