from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
from src.ui.mainwindow_ui import Ui_MainWindow
from src.views.user import User
from src.views.re_product import REProduct


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())

        self.set_ui()

    def set_ui(self):
        self.user_page = User()
        self.re_page = REProduct()
        self.content_container.addWidget(self.user_page)
        self.content_container.addWidget(self.re_page)
        self.content_container.setCurrentIndex(1)
