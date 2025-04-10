import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.services.re_service import RESettingService
from src import constants

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()

    print(RESettingService.read_all(constants.RE_SETTING_WARDS_TABLE))
