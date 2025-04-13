# # src/controllers/re_controller_utils.py
# import uuid
# import os
# from PyQt6.QtWidgets import QMessageBox

# from src import constants
# from src.services.re_service import (
#     REImageDirService,
#     RETemplateService,
# )

# from src.services import service_utils


# def get_image_path(record_id):
#     img_row = REImageDirService.read({"is_selected": 1})
#     img_dir = os.path.join(img_row.get("value"), str(record_id))
#     return service_utils.get_images_in_directory(os.path.abspath(img_dir))
