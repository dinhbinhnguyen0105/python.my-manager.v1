import json
import os


class RealEstateProductConfigs:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            _path = os.path.dirname(__file__)
            with open(
                os.path.join(_path, "real_estate_product.json"), "r", encoding="utf-8"
            ) as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return []

    def options(self):
        if not self.data:
            return []
        return self.data.get("options", [])

    def categories(self):
        if not self.data:
            return []
        return self.data.get("categories", [])

    def provinces(self):
        if not self.data:
            return []
        return self.data.get("provinces", [])

    def districts(self):
        if not self.data:
            return []
        return self.data.get("districts", [])

    def wards(self):
        if not self.data:
            return []
        return self.data.get("wards", [])

    def building_line_s(self):
        if not self.data:
            return []
        return self.data.get("building_line_s", [])

    def legal_s(self):
        if not self.data:
            return []
        return self.data.get("legal_s", [])

    def furniture_s(self):
        if not self.data:
            return []
        return self.data.get("furniture_s", [])

    def image_dir(self):
        if not self.data:
            return ""
        _path = os.path.dirname(__file__)
        image_dir = self.data.get("image_directory", "")
        if not image_dir:
            return os.path.join(_path, "..", "repositories", "images")
        return image_dir

    def allowed_values(self):
        return self.data.get("allowed_values", {})
