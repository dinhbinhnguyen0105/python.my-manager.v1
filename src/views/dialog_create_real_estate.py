from PyQt6.QtCore import Qt, QMimeData
# Import QPixmap for displaying images
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel  # Import QDialog and QLabel
from src.ui.dialog_create_real_estate_ui import Ui_DialogCreateRealEstate
from src.configs.real_estate_product import RealEstateProductConfigs


# Inherit from QDialog
class DialogCreateRealEstate(QDialog, Ui_DialogCreateRealEstate):
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize QDialog
        self.image_path = []
        self.setupUi(self)

        self.setWindowTitle("Create Real Estate")
        self.setFixedSize(self.size())

        self.legal.setDisabled(True)
        self.buttonBox.setDisabled(True)

        self.sell.clicked.connect(
            lambda: self._setupUi("sell"))
        self.rent.clicked.connect(
            lambda: self._setupUi("rent"))
        self.assignment.clicked.connect(
            lambda: self._setupUi("assignment"))

        # Connect signals to slots
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)

        self.setupImageDrop()

    def _setupUi(self, option):
        self.buttonBox.setDisabled(False)
        self.option = option
        self.setupComboBox()
        if option == "rent" or option == "assignment":
            self.legal.setDisabled(True)
        else:
            self.legal.setDisabled(False)

    def setupComboBox(self):
        # Setup combo boxes with data from RealEstateProductConfigs
        configs = RealEstateProductConfigs()
        # category
        self.category.clear()
        for category in configs.categories():
            self.category.addItem(category.get(
                "name")[0].capitalize(), category.get("value"))
        # province
        self.province.clear()
        for province in configs.provinces():
            self.province.addItem(province.get(
                "name")[0].capitalize(), province.get("value"))

        # district
        self.district.clear()
        for district in configs.districts():
            self.district.addItem(district.get(
                "name")[0].capitalize(), district.get("value"))
        # ward
        self.ward.clear()
        for ward in configs.wards():
            self.ward.addItem(ward.get(
                "name")[0].capitalize(), ward.get("value"))
        # building_line
        self.building_line.clear()
        for building_line in configs.building_line_s():
            self.building_line.addItem(building_line.get(
                "name")[0].capitalize(), building_line.get("value"))
        # legal
        self.legal.clear()
        for legal in configs.legal_s():
            self.legal.addItem(legal.get(
                "name")[0].capitalize(), legal.get("value"))
        # furniture
        self.furniture.clear()
        for furniture in configs.furniture_s():
            self.furniture.addItem(furniture.get(
                "name")[0].capitalize(), furniture.get("value"))

    def on_accept(self):
        # Handle the accept button click
        print(self.province.currentData())
        pass

    def on_reject(self):
        # Handle the reject button click
        pass

    def setupImageDrop(self):
        # Configure self.images as a drag-and-drop widget
        self.images.setAcceptDrops(True)

        # Override dragEnterEvent and dropEvent for self.images
        self.images.dragEnterEvent = self.imagesDragEnterEvent
        self.images.dropEvent = self.imagesDropEvent

    def imagesDragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def imagesDropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            self.image_path = [url.toLocalFile()
                               for url in event.mimeData().urls()]

            self.handleDroppedImages(self.image_path)

    def handleDroppedImages(self, image_paths):
        # Handle the dropped image paths
        print("Dropped images:", image_paths)
        if image_paths:
            # Display the first image in self.images
            pixmap = QPixmap(image_paths[0])
            if not pixmap.isNull():
                self.images.setPixmap(pixmap.scaled(
                    self.images.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                self.images.setText("Failed to load image.")
        else:
            self.images.setText("No images dropped.")
