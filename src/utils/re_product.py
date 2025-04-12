from src.controllers.re_controller import RETemplateController
from src import constants


def init_title(data, default=1):
    controller_template = RETemplateController(
        constants.RE_TEMPLATE_TITLE_TABLE)
    if default:
        title_template = controller_template.read(0)
    else:

    pass


def init_description(data, default=-1):

    pass
