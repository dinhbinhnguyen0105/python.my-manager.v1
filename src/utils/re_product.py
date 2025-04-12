import sys
import os
import subprocess
import platform
from random import randint
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from src import constants
from src.controllers.re_controller import RETemplateController, RESettingController


def init_template(table_name, raw_data, default=True):
    if table_name == constants.RE_TEMPLATE_TITLE_TABLE:
        controller_template = RETemplateController(constants.RE_TEMPLATE_TITLE_TABLE)
    elif table_name == constants.RE_TEMPLATE_DESCRIPTION_TABLE:
        controller_template = RETemplateController(
            constants.RE_TEMPLATE_DESCRIPTION_TABLE
        )
    if default:
        template_raw = controller_template.read(0)
    else:
        template_ids = controller_template.get_ids_by_condition(
            {"option_id": raw_data.get("option_id")}
        )
        random_title = template_ids[randint(0, len(template_ids) - 1)]
        template_raw = controller_template.read(random_title)

    raw_template = template_raw.get("value")
    template = _relay_keyword(raw_data, raw_template)
    return {
        "template": template,
        "tid": template_raw.get("tid"),
    }


def init_footer(pid, updated_at, title_info, description_info):
    return f"""
[
    pid <{pid}>
    updated_at <{updated_at}>
    tid.title <{title_info}>
    tid.description <{description_info}>
]
"""


def _relay_keyword(raw_data, template: str):
    keyword_values = _get_value(raw_data)
    if keyword_values.get("option").get("value") == "sell":
        raw_data.setdefault("unit", "tỷ")
    elif (
        keyword_values.get("option").get("value") == "rent"
        or keyword_values.get("option").get("value") == "assignment"
    ):
        raw_data.setdefault("unit", "triệu/tháng")

    template = template.replace(
        "<option>", keyword_values.get("option").get("label_vi")
    )
    template = template.replace(
        "<category>", keyword_values.get("category").get("label_vi")
    )
    template = template.replace(
        "<province>", keyword_values.get("province").get("label_vi").title()
    )
    template = template.replace(
        "<district>", keyword_values.get("district").get("label_vi").title()
    )
    template = template.replace(
        "<ward>", keyword_values.get("ward").get("label_vi").title()
    )
    template = template.replace("<legal>", keyword_values.get("legal").get("label_vi"))
    template = template.replace(
        "<furniture>", keyword_values.get("furniture").get("label_vi")
    )
    template = template.replace(
        "<building_line>", keyword_values.get("building_line").get("label_vi")
    )
    template = template.replace("<price>", str(raw_data.get("price")))
    template = template.replace("<PID>", raw_data.get("pid"))
    template = template.replace("<street>", raw_data.get("street").title())
    template = template.replace("<structure>", str(raw_data.get("structure")) + " tầng")
    template = template.replace("<function>", raw_data.get("function"))
    template = template.replace("<description>", raw_data.get("description"))
    template = template.replace("<unit>", raw_data.get("unit"))
    template = template.replace("<area>", str(raw_data.get("area")) + "m2")

    icon = constants.ICONS[randint(0, len(constants.ICONS) - 1)]
    while template != template.replace("<icon>", icon, 1):
        icon = constants.ICONS[randint(0, len(constants.ICONS) - 1)]
        template = template.replace("<icon>", icon, 1)

    return template


def _get_value(data):
    option = RESettingController.static_read(
        constants.RE_SETTING_OPTIONS_TABLE, data.get("option_id")
    )
    category = RESettingController.static_read(
        constants.RE_SETTING_CATEGORIES_TABLE, data.get("category_id")
    )
    province = RESettingController.static_read(
        constants.RE_SETTING_PROVINCES_TABLE, data.get("province_id")
    )
    district = RESettingController.static_read(
        constants.RE_SETTING_DISTRICTS_TABLE, data.get("district_id")
    )
    ward = RESettingController.static_read(
        constants.RE_SETTING_WARDS_TABLE, data.get("ward_id")
    )
    legal = RESettingController.static_read(
        constants.RE_SETTING_LEGAL_S_TABLE, data.get("legal_id")
    )
    furniture = RESettingController.static_read(
        constants.RE_SETTING_FURNITURE_S_TABLE, data.get("furniture_id")
    )
    building_line = RESettingController.static_read(
        constants.RE_SETTING_BUILDING_LINE_S_TABLE, data.get("building_line_id")
    )

    return {
        "option": option,
        "category": category,
        "province": province,
        "district": district,
        "ward": ward,
        "legal": legal,
        "furniture": furniture,
        "building_line": building_line,
    }


def open_dir(path_dir):
    folder_path = os.path.dirname(path_dir)
    QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
    if sys.platform == "win32":
        subprocess.run(["explorer", os.path.dirname(path_dir)], check=True)
    elif sys.platform == "darwin":
        subprocess.run(["open", os.path.dirname(path_dir)], check=True)
    else:
        subprocess.Popen(["xdg-open", os.path.dirname(path_dir)])
