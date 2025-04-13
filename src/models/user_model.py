# src/models/user_model.py
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt
from src import constants


class BasicModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def get_record_ids(self, rows):
        ids = []
        for row in rows:
            if 0 <= row < self.rowCount():
                index = self.index(row, self.fieldIndex("id"))
                ids.append(self.data(index))
        return ids


class UserModel(BasicModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable(constants.USER_TABLE)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()


class UserDataDirModel(BasicModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable(constants.USER_SETTING_USER_DATA_DIR_TABLE)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()


class UserProxyModel(BasicModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable(constants.USER_SETTING_PROXY_TABLE)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()
