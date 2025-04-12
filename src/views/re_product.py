# src/views/re_product.py
import os
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget, QMenu, QFileDialog
from PyQt6.QtGui import QAction, QPixmap

from src.ui.re_product_ui import Ui_REProduct
from src.models.re_model import REProductModel
from src.controllers.re_controller import (
    REProductController,
    RESettingController,
    RETemplateController,
)
from src.views.dialog_re_product import DialogREProduct
from src.views.dialog_re_template_settings import DialogRETemplateSetting
from src.views.dialog_re_product_settings import DialogREProductSetting
from src.utils import re_product as re_product_utils
from src import constants


class REProduct(QWidget, Ui_REProduct):
    image_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self.model = REProductModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.controller_product = REProductController(self.model)
        self.raw_data = None
        self.setup_ui()
        self.setup_events()

    def setup_ui(self):
        self.setup_table()
        self.setup_comboboxes()

    def setup_comboboxes(self):
        wards = RESettingController.static_read_all(constants.RE_SETTING_WARDS_TABLE)
        options = RESettingController.static_read_all(
            constants.RE_SETTING_OPTIONS_TABLE
        )
        categories = RESettingController.static_read_all(
            constants.RE_SETTING_CATEGORIES_TABLE
        )
        building_line_s = RESettingController.static_read_all(
            constants.RE_SETTING_BUILDING_LINE_S_TABLE
        )
        furniture_s = RESettingController.static_read_all(
            constants.RE_SETTING_FURNITURE_S_TABLE
        )
        legal_s = RESettingController.static_read_all(
            constants.RE_SETTING_LEGAL_S_TABLE
        )

        for ward in wards:
            name = ward.get("label_vi").capitalize()
            value = ward.get("label_vi")
            self.wards_combobox.addItem(name, value)
        for option in options:
            name = option.get("label_vi").capitalize()
            value = option.get("label_vi")
            self.options_combobox.addItem(name, value)
        for category in categories:
            name = category.get("label_vi").capitalize()
            value = category.get("label_vi")
            self.categories_combobox.addItem(name, value)
        for building_line in building_line_s:
            name = building_line.get("label_vi").capitalize()
            value = building_line.get("label_vi")
            self.building_line_s_combobox.addItem(name, value)
        for furniture in furniture_s:
            name = furniture.get("label_vi").capitalize()
            value = furniture.get("label_vi")
            self.furniture_s_combobox.addItem(name, value)
        for legal in legal_s:
            name = legal.get("label_vi").capitalize()
            value = legal.get("label_vi")
            self.legal_s_combobox.addItem(name, value)

    def setup_events(self):
        self.setup_filters()
        self.action_create_btn.clicked.connect(self.handle_create)
        self.action_settings_btn.clicked.connect(self.handle_product_settings)
        self.action_templates_btn.clicked.connect(self.handle_template_settings)
        self.products_table.selectionModel().selectionChanged.connect(
            self.setup_details
        )
        self.image_label.mousePressEvent = self.image_label_click_event
        self.action_default_btn.clicked.connect(lambda: self.set_detail_content(True))
        self.action_random_btn.clicked.connect(lambda: self.set_detail_content(False))

    def image_label_click_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.image_clicked.emit()
        super().mousePressEvent(event)

    def setup_filters(self):
        self.pid_input.textChanged.connect(
            lambda: self.apply_column_filter(self.pid_input.text(), 1)
        )
        self.street_input.textChanged.connect(
            lambda: self.apply_column_filter(self.street_input.text(), 5)
        )
        self.price_input.textChanged.connect(
            lambda: self.apply_column_filter(self.price_input.text(), 8)
        )
        self.function_input.textChanged.connect(
            lambda: self.apply_column_filter(self.function_input.text(), 13)
        )
        self.structure_input.textChanged.connect(
            lambda: self.apply_column_filter(self.structure_input.text(), 12)
        )
        self.area_input.textChanged.connect(
            lambda: self.apply_column_filter(self.area_input.text(), 7)
        )

        self.options_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.options_combobox.currentData(), 3)
        )
        self.wards_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.wards_combobox.currentData(), 4)
        )
        self.categories_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.categories_combobox.currentData(), 6)
        )
        self.legal_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.legal_s_combobox.currentData(), 9)
        )
        self.building_line_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(
                self.building_line_s_combobox.currentData(), 14
            )
        )
        self.furniture_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(
                self.furniture_s_combobox.currentData(), 15
            )
        )

    def setup_details(self):
        id = self.get_selected_id()
        if id is None:
            return
        self.raw_data = self.controller_product.read_product(id, raw=True)
        image_paths = self.controller_product.get_image_paths(id)
        self.set_detail_content(True)
        if len(image_paths):
            self.display_image(image_paths[0])
            self.image_clicked.connect(
                lambda: self.handle_open_image_dir(image_paths[0])
            )

    def set_detail_content(self, default=True):
        if not self.raw_data:
            return False
        title_raw = re_product_utils.init_template(
            constants.RE_TEMPLATE_TITLE_TABLE, self.raw_data, default
        )
        description_raw = re_product_utils.init_template(
            constants.RE_TEMPLATE_DESCRIPTION_TABLE, self.raw_data, default
        )
        footer = re_product_utils.init_footer(
            self.raw_data.get("pid"),
            self.raw_data.get("updated_at"),
            title_raw.get("tid"),
            description_raw.get("tid"),
        )
        self.detail_text.setPlainText(
            title_raw.get("template").upper()
            + "\n"
            + description_raw.get("template")
            + footer
        )

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.image_label.setText("Failed to load image.")

    def handle_open_image_dir(self, image_path):
        if image_path:
            re_product_utils.open_dir(image_path)

    def apply_column_filter(self, filter_text, column_index):
        if (
            filter_text == "Tất cả" or not filter_text
        ):  # Giả sử "Tất cả" hoặc rỗng là để bỏ lọc
            self.proxy_model.setFilterFixedString("")
        else:
            self.proxy_model.setFilterFixedString(filter_text)
            self.proxy_model.setFilterKeyColumn(column_index)

    def setup_table(self):
        self.products_table.setModel(self.proxy_model)
        self.products_table.setSelectionBehavior(
            self.products_table.SelectionBehavior.SelectRows
        )
        self.products_table.setSelectionMode(
            self.products_table.SelectionMode.SingleSelection
        )
        # self.products_table.resizeColumnsToContents()
        self.products_table.setSortingEnabled(True)

        self.products_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)

        self.products_table.setColumnHidden(0, True)
        self.products_table.setColumnHidden(10, True)
        self.products_table.setColumnHidden(11, True)
        self.products_table.setColumnHidden(16, True)
        self.products_table.setColumnHidden(17, True)
        self.products_table.setColumnHidden(18, True)

        self.products_table.horizontalHeader()

    def show_context_menu(self, pos: QPoint):
        global_pos = self.products_table.mapToGlobal(pos)
        menu = QMenu(self.products_table)
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)

        edit_action.triggered.connect(self.handle_edit)
        delete_action.triggered.connect(self.handle_delete)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.popup(global_pos)

    def get_selected_id(self):
        selected_proxy_indexes = self.products_table.selectionModel().selectedRows()
        if not selected_proxy_indexes:
            return None
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        row = source_index.row()
        if 0 <= row < self.model.rowCount():
            return self.model.get_record_id(row)
        return None

    def handle_create(self):
        create_dialog = DialogREProduct()
        create_dialog.setWindowTitle("Create Product")
        create_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        create_dialog.setFixedSize(create_dialog.size())
        create_dialog.accepted.connect(
            lambda: self.controller_product.add_product(create_dialog.fields)
        )
        create_dialog.exec()

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
                self.controller_product.delete_product(id)
            else:
                QMessageBox.warning(self, "Warning", "No product selected.")
        else:
            # User clicked No, do nothing
            pass

    def handle_edit(self):
        id = self.get_selected_id()
        if id is not None:
            current_product_data = self.controller_product.read_product(id)
            image_paths = self.controller_product.get_image_paths(id)
            current_product_data.setdefault("image_paths", image_paths)
            edit_dialog = DialogREProduct(current_product_data)
            edit_dialog.setWindowTitle("Edit Product")
            edit_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            edit_dialog.setFixedSize(edit_dialog.size())
            edit_dialog.accepted.connect(
                lambda: self.controller_product.update_product(id, edit_dialog.fields)
            )
            edit_dialog.exec()

        else:
            QMessageBox.warning(self, "Warning", "No product selected.")
        pass

    def handle_template_settings(self):
        template_settings_dialog = DialogRETemplateSetting()
        template_settings_dialog.setWindowTitle("setting template".title())
        template_settings_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        template_settings_dialog.setFixedSize(template_settings_dialog.size())
        template_settings_dialog.exec()

    def handle_product_settings(self):
        product_settings_dialog = DialogREProductSetting()
        product_settings_dialog.setWindowTitle("setting product".title())
        product_settings_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        product_settings_dialog.setFixedSize(product_settings_dialog.size())
        product_settings_dialog.exec()
