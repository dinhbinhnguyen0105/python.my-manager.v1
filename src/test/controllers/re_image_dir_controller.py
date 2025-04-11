import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.controllers.re_controller import REImageDirController
from src.models.re_model import BaseSettingModel
from src import constants

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()

    # model = BaseSettingModel(constants.RE_SETTING_IMG_DIR_TABLE)
    controller = REImageDirController(constants.RE_SETTING_IMG_DIR_TABLE)

    is_selected = controller.read({"is_selected": 1})
    print(is_selected)
