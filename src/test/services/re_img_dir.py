import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.services.re_service import REImageDirService
from src import constants

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()
    # REImageDirService.create(
    #     {"value": "/Users/ndb/Dev/python/python.my-manager.v1", "is_selected": 0}
    # )
    # REImageDirService.delete(1)

    # REImageDirService.update(3, {"value": "4"})
    # print(REImageDirService.read_all())
    print(REImageDirService.read({"is_selected": 1}))
