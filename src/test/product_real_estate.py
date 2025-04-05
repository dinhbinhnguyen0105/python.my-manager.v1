import sys
from PyQt6.QtWidgets import QApplication, QWidget
from src.views.product_real_estate import ProductRealEstate
from src.models.real_estate_database import initialize_products_database

if __name__ == "__main__":

    app = QApplication(sys.argv)
    initialize_products_database()

    window = ProductRealEstate()
    window.show()
    sys.exit(app.exec())
