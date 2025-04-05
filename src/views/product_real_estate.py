# src/views/product_real_estate.py
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel
from PyQt6.QtWidgets import (
    QMessageBox,
    QDialog,
    QWidget,
    QMenu,
    QTableView,
    QAbstractItemView,
)
from PyQt6.QtGui import QAction


from src.ui.product_real_estate_ui import Ui_ProductRealEstate
from src.models.real_estate_model import RealEstateProductModel
from src.controllers.real_estate_controller import RealEstateController
from src.views.dialog_create_update_real_estate import DialogCreateUpdateRealEstate


class ProductRealEstate(QWidget, Ui_ProductRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self.model = RealEstateProductModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.control = RealEstateController(self.model)
        self.setup_ui()

    def setup_ui(self):
        self.setup_table()
        self.setup_buttons()
        pass

    def setup_table(self):
        self.products_table.setModel(self.proxy_model)
        self.products_table.setSelectionBehavior(
            self.products_table.SelectionBehavior.SelectRows
        )
        self.products_table.setSelectionMode(
            self.products_table.SelectionMode.SingleSelection
        )
        self.products_table.resizeColumnsToContents()
        self.products_table.setSortingEnabled(True)

        self.products_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)

        self.products_table.setColumnHidden(0, True)
        self.products_table.setColumnHidden(2, True)
        self.products_table.setColumnHidden(3, True)
        self.products_table.setColumnHidden(14, True)
        self.products_table.setColumnHidden(17, True)

        self.products_table.selectionModel().selectionChanged.connect(
            self.setup_details
        )

    def setup_buttons(self):
        self.action_create_btn.clicked.connect(self.handle_crete)

    def filter_logics(self, row, parent, conditions):
        source_model = self.proxy_model.sourceModel()

    def show_context_menu(self, pos: QPoint):
        global_pos = self.products_table.mapToGlobal(pos)
        menu = QMenu(self.products_table)
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)

        edit_action.triggered.connect(self.handle_update)
        delete_action.triggered.connect(self.handle_delete)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.popup(global_pos)
        # menu.exec(global_pos)

    def get_selected_id(self):
        selected_indexes = self.products_table.selectionModel().selectedRows()
        if selected_indexes:
            row = selected_indexes[0].row()
            if row is not None:
                record = self.model.record(row)
                return record.value("id")
        return None

    def handle_update(self):
        id = self.get_selected_id()
        edit_dialog = DialogCreateUpdateRealEstate()
        edit_dialog.setWindowTitle("Edit Product")
        edit_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        edit_dialog.setFixedSize(edit_dialog.size())
        if id is not None:
            data = self.control.read_product(id)
            edit_dialog.load_fields(data)
            edit_dialog.accepted.connect(
                lambda: self.control.update_product(edit_dialog.get_fields())
            )
            edit_dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "No product selected.")
        pass

    def handle_delete(self):
        id = self.get_selected_id()
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if id is not None:
                self.control.delete_product(id)
                self.model.select()
            else:
                QMessageBox.warning(self, "Warning", "No product selected.")
        else:
            # User clicked No, do nothing
            pass

    def handle_crete(self):
        create_dialog = DialogCreateUpdateRealEstate()
        create_dialog.setWindowTitle("Create Product")
        create_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        create_dialog.setFixedSize(create_dialog.size())
        create_dialog.accepted.connect(
            lambda: self.control.add_product(create_dialog.get_fields())
        )
        create_dialog.exec()

    def setup_details(self):
        id = self.get_selected_id()
        if id is None:
            return
        data = self.control.read_product(id)
        image_paths = self.control.get_image_path(id)
