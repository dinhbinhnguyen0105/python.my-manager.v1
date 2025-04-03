import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QMessageBox
from src.controllers.real_estate_controller import RealEstateController
from src.models.real_estate_model import RealEstateProductModel
from src._types import RealEstateProductType


class TestRealEstateController(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock(spec=RealEstateProductModel)
        self.controller = RealEstateController(self.mock_model)

    @patch("src.services.real_estate_services.RealEstateProductService.create")
    def test_add_product_success(self, mock_create):
        mock_create.return_value = True
        data = {"name": "Test Product", "price": 1000}

        with patch.object(QMessageBox, "information") as mock_info:
            self.controller.add_product(data)
            mock_create.assert_called_once_with(data)
            self.mock_model.select.assert_called_once()
            mock_info.assert_called_once_with(
                None, "Success", "Real estate product added successfully."
            )

    @patch("src.services.real_estate_services.RealEstateProductService.create")
    def test_add_product_failure(self, mock_create):
        mock_create.side_effect = Exception("Error occurred")
        data = {"name": "Test Product", "price": 1000}

        with patch.object(QMessageBox, "critical") as mock_critical:
            self.controller.add_product(data)
            mock_create.assert_called_once_with(data)
            mock_critical.assert_called_once_with(
                None, "Error", "Error occurred")

    @patch("src.services.real_estate_services.RealEstateProductService.read")
    def test_read_product_success(self, mock_read):
        mock_read.return_value = {"id": "1", "name": "Test Product"}
        pid = "1"

        product = self.controller.read_product(pid)
        mock_read.assert_called_once_with(pid)
        self.assertEqual(product, {"id": "1", "name": "Test Product"})

    @patch("src.services.real_estate_services.RealEstateProductService.read")
    def test_read_product_not_found(self, mock_read):
        mock_read.return_value = None
        pid = "1"

        with patch.object(QMessageBox, "warning") as mock_warning:
            product = self.controller.read_product(pid)
            mock_read.assert_called_once_with(pid)
            mock_warning.assert_called_once_with(
                None, "Warning", "Product not found.")
            self.assertIsNone(product)

    @patch("src.services.real_estate_services.RealEstateProductService.update")
    def test_update_product_success(self, mock_update):
        mock_update.return_value = True
        data = {"id": "1", "name": "Updated Product"}

        with patch.object(QMessageBox, "information") as mock_info:
            result = self.controller.update_product(data)
            mock_update.assert_called_once_with(data)
            self.mock_model.select.assert_called_once()
            mock_info.assert_called_once_with(
                None, "Success", "Real estate product updated successfully."
            )
            self.assertTrue(result)

    @patch("src.services.real_estate_services.RealEstateProductService.delete")
    def test_delete_product_success(self, mock_delete):
        mock_delete.return_value = True
        pid = "1"

        with patch.object(QMessageBox, "information") as mock_info:
            result = self.controller.delete_product(pid)
            mock_delete.assert_called_once_with(pid)
            self.mock_model.select.assert_called_once()
            mock_info.assert_called_once_with(
                None, "Success", "Real estate product deleted successfully."
            )
            self.assertTrue(result)

    @patch("src.services.real_estate_services.RealEstateProductService.delete")
    def test_delete_product_failure(self, mock_delete):
        mock_delete.return_value = False
        pid = "1"

        with patch.object(QMessageBox, "warning") as mock_warning:
            result = self.controller.delete_product(pid)
            mock_delete.assert_called_once_with(pid)
            mock_warning.assert_called_once_with(
                None, "Warning", "Failed to delete product."
            )
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
