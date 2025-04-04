from PyQt6.QtWidgets import QApplication, QMessageBox
from src.views.dialog_create_update_real_estate import DialogCreateUpdateRealEstate
from src.models.real_estate_database import initialize_products_database
from src.models.real_estate_model import RealEstateProductModel
from src.controllers.real_estate_controller import RealEstateController


def handle_save(new_product):
    print(new_product)
    model = RealEstateProductModel()
    controller = RealEstateController(model)
    controller.add_product(new_product)


def handle_update(new_data):
    # print(new_data)
    model = RealEstateProductModel()
    controller = RealEstateController(model)
    print(controller.update_product(new_data))


if __name__ == "__main__":
    app = QApplication([])
    initialize_products_database()

    dialog = DialogCreateUpdateRealEstate()
    dialog.show()

    model = RealEstateProductModel()
    controller = RealEstateController(model)
    data = controller.read_product(4)
    # print(data)
    # exit()

    # print(controller.read_all_product())
    dialog.load_fields(data)

    # Đọc ghi luôn dựa trên id, vì khi update pid có thể thay đổi

    # dialog.accepted.connect(lambda: handle_save(dialog.get_fields()))
    dialog.accepted.connect(lambda: handle_update(dialog.get_fields()))
    dialog.rejected.connect(lambda: print("Dialog rejected"))
    app.exec()
