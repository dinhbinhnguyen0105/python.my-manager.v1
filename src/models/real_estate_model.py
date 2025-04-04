# src/models/real_estate_model.py
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt
from src.constants import REAL_ESTATE_PRODUCT_TABLE, REAL_ESTATE_TEMPLATE_TABLE


class RealEstateProductModel(QSqlTableModel):
    def __init__(self):
        super().__init__()
        self.setTable(REAL_ESTATE_PRODUCT_TABLE)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.select()

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class RealEstateTemplateModel(QSqlTableModel):
    pass
