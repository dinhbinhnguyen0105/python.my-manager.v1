# src/views/user.py
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget, QMenu, QDialog
from PyQt6.QtGui import QAction

from src.ui.user_ui import Ui_User
from src.models.user_model import UserModel
from src.controllers.user_controller import UserController
from src.views.dialog_user_create import DialogUserCreate
from src.views.dialog_user_settings import DialogUserSettings


class User(QWidget, Ui_User):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("user".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self.model = UserModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.controller_user = UserController(self.model)

        self.set_ui()
        self.set_events()

    def set_ui(self):
        self.set_table()

    def set_events(self):
        self.create_new_btn.clicked.connect(self.handle_create)
        self.settings_btn.clicked.connect(self.handle_settings)

    def set_table(self):
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSelectionBehavior(
            self.table_view.SelectionBehavior.SelectRows
        )

        self.table_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.horizontalHeader()

        self.table_view.setSortingEnabled(True)

        self.table_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(
            self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        global_pos = self.table_view.mapToGlobal(pos)
        menu = QMenu(self.table_view)
        launch_action = QAction("Launch browser", self)
        delete_action = QAction("Delete", self)

        launch_action.triggered.connect(self.handle_launch_browser)
        delete_action.triggered.connect(self.handle_delete)

        menu.addAction(launch_action)
        menu.addAction(delete_action)

        menu.popup(global_pos)

    def handle_launch_browser(self): pass

    def handle_delete(self):
        selected_ids = self.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(self, "Warning", "No users selected.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete these users: {', '.join(map(str, selected_ids))}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller_user.deletes(selected_ids)
        else:
            pass

    def handle_create(self):
        dialog_create = DialogUserCreate()
        dialog_create.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        dialog_create.setFixedSize(dialog_create.size())
        if dialog_create.exec() == QDialog.DialogCode.Accepted:
            self.controller_user.create(dialog_create.fields)

    def handle_settings(self):
        dialog_settings = DialogUserSettings()
        dialog_settings.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        dialog_settings.setFixedSize(dialog_settings.size())
        dialog_settings.exec()

    def get_selected_ids(self):
        selected_proxy_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_proxy_indexes:
            return None

        source_indexes = [self.proxy_model.mapToSource(
            proxy_index) for proxy_index in selected_proxy_indexes]
        rows = [source_index.row() for source_index in source_indexes]
        return self.model.get_record_ids(rows)
