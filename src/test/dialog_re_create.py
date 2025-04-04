from PyQt6.QtWidgets import QApplication
from src.views.dialog_create_real_estate import DialogCreateRealEstate
from src.models.real_estate_database import initialize_products_database
from src.models.real_estate_model import RealEstateProductModel
from src.controllers.real_estate_controller import RealEstateController


def handle_accepted(new_product):
    print(new_product)
    # model = RealEstateProductModel()
    # controller = RealEstateController(model)
    # controller.add_product(new_product)


if __name__ == "__main__":
    app = QApplication([])
    initialize_products_database()
    # model = RealEstateProductModel()
    # controller = RealEstateController(model)
    # print(controller.read_all_product())
    dialog = DialogCreateRealEstate()
    dialog.show()
    dialog.accepted.connect(lambda: handle_accepted(dialog.get_fields()))
    dialog.rejected.connect(lambda: print("Dialog rejected"))
    app.exec()
