import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableView,
    QMainWindow,
    QLineEdit,
    QPushButton,
)

from src.models.real_estate_database import initialize_products_database
from src.controllers.real_estate_controller import RealEstateController
from src.models.real_estate_model import RealEstateProductModel

from src.services.real_estate_services import RealEstateProductService


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        centrall_widget = QWidget()
        self.setCentralWidget(centrall_widget)
        layout = QVBoxLayout()
        centrall_widget.setLayout(layout)

        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText("Enter Product ID")
        layout.addWidget(self.pid_input)

        self.option_input = QLineEdit(self)
        self.option_input.setPlaceholderText("Enter Option")
        layout.addWidget(self.option_input)

        self.model = RealEstateProductModel()
        self.controller = RealEstateController(self.model)

        print(RealEstateProductService.get_columns())
        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)
        # Hide unwanted columns
        # Example: Hides the first column
        self.table_view.setColumnHidden(0, True)
        # Example: Hides the third column
        self.table_view.setColumnHidden(2, True)
        self.table_view.setColumnHidden(3, True)
        layout.addWidget(self.table_view)

        self.add_btn = QPushButton("Add Product", self)
        layout.addWidget(self.add_btn)
        self.add_btn.clicked.connect(self.add_product)

    def add_product(self):
        pid = self.pid_input.text()
        option = self.option_input.text()
        data = {"pid": pid, "option": option}
        self.controller.add_product(data)
        self.model.select()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not initialize_products_database():
        raise Exception("Failed to initialize the database.")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
