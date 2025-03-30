# src/models/user_model.py
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt


class UserModel(QSqlTableModel):
    def __init__(self):
        super().__init__()
        self.setTable("users")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.select()

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
