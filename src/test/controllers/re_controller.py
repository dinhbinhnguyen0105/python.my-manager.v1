import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.controllers.re_controller import REProductController
from src.models.re_model import REProductModel
from src import constants

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()
    model = REProductModel()
    controller = REProductController(model)

    controller.add_product({
        "pid": "unique_pid_3",
        "status_id": 1,
        "option_id": 1,
        "ward_id": 1,
        "street": "Main Street",
        "category_id": 1,
        "area": 100.5,
        "price": 250000.00,
        "legal_id": 1,
        "province_id": 1,
        "district_id": 1,
        "structure": 2,
        "function": "Residential",
        "building_line_id": 1,
        "furniture_id": 1,
        "description": "A lovely property",
        "image_paths": [
            "/Volumes/KINGSTON/Images/thumbnail/3.jpeg",
            "/Volumes/KINGSTON/Images/thumbnail/4.jpeg",
            "/Volumes/KINGSTON/Images/thumbnail/5.jpeg",
            "/Volumes/KINGSTON/Images/thumbnail/m2.jpeg",
            "/Volumes/KINGSTON/Images/thumbnail/m3.jpeg",
            "/Volumes/KINGSTON/Images/thumbnail/thumbnail.jpg",

        ],
    })

    print(controller.read_all_product())
