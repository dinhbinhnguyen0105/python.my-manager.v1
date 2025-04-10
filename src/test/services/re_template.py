import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.services.re_service import RETemplateService
from src import constants

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()
    # RETemplateService().create(constants.RE_TEMPLATE_TITLE_TABLE, {
    #     "tid": "1",
    #     "option_id": 1,
    #     "value": "1"
    # })

    title_templates = RETemplateService.read_all(
        constants.RE_TEMPLATE_TITLE_TABLE)
    print(title_templates)

    # print(RETemplateService.read(constants.RE_TEMPLATE_TITLE_TABLE, 0))
