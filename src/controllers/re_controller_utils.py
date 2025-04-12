# src/controllers/re_controller_utils.py
import uuid
import os
from PyQt6.QtWidgets import QMessageBox

from src import constants
from src.services.re_service import (
    REImageDirService,
    RETemplateService,
)

from src.services import re_service_utils


def generate_pid(option):
    try:
        while True:
            uuid_str = str(uuid.uuid4())
            pid = uuid_str.replace("-", "")[:8]
            if option.lower() == "sell":
                pid = "S." + pid
            elif option.lower() == "rent":
                pid = "R." + pid
            elif option.lower() == "assignment":
                pid = "A." + pid
            else:
                raise ValueError("Invalid option")
            pid = ("RE." + pid).lower()
            if not re_service_utils.is_value_existed(
                constants.RE_PRODUCT_TABLE, {"pid": pid}
            ):
                return pid
            else:
                continue
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        raise Exception("Failed to generate PID.")


def generate_tid(table_name):
    try:
        while True:
            uuid_str = str(uuid.uuid4())
            tid = uuid_str.replace("-", "")[:8]
            if table_name == constants.RE_TEMPLATE_TITLE_TABLE:
                tid = "T.T." + tid
            elif table_name == constants.RE_TEMPLATE_DESCRIPTION_TABLE:
                tid = "T.D." + tid
            if not re_service_utils.is_value_existed(table_name, {"tid": tid}):
                return tid
            else:
                continue
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        raise Exception("Failed to generate TID.")


def validate_new_product(data):
    print(data)
    if not data.get("pid") or re_service_utils.is_value_existed(constants.RE_PRODUCT_TABLE, {"pid": data.get("pid")}):
        QMessageBox.critical(None, "Error", "Invalid pid.")
        return False
    if (
        not isinstance(data.get("area"), (int, float))
        or not isinstance(data.get("structure"), (int, float))
        or not isinstance(data.get("price"), (int, float))
    ):
        QMessageBox.critical(
            None, "Error", "Area, structure, and price must be numbers."
        )
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_STATUSES_TABLE, {"id": data.get("status_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid status selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_PROVINCES_TABLE, {"id": data.get("province_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid province selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_DISTRICTS_TABLE, {"id": data.get("district_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid district selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_WARDS_TABLE, {"id": data.get("ward_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid ward selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_OPTIONS_TABLE, {"id": data.get("option_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid option selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_CATEGORIES_TABLE, {"id": data.get("category_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid category selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_BUILDING_LINE_S_TABLE,
        {"id": data.get("building_line_id")},
    ):
        QMessageBox.critical(None, "Error", "Invalid building_line selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_FURNITURE_S_TABLE,
        {"id": data.get("furniture_id")},
    ):
        QMessageBox.critical(None, "Error", "Invalid furniture selected.")
        return False
    if not re_service_utils.is_value_existed(
        constants.RE_SETTING_LEGAL_S_TABLE, {"id": data.get("legal_id")}
    ):
        QMessageBox.critical(None, "Error", "Invalid legal selected.")
        return False
    return True


def get_image_path(record_id):
    img_row = REImageDirService.read({"is_selected": 1})
    img_dir = os.path.join(img_row.get("value"), str(record_id))
    return re_service_utils.get_images_in_directory(os.path.abspath(img_dir))


def get_columns():
    return re_service_utils.get_columns(constants.RE_PRODUCT_TABLE)
