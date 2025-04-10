# test
import logging
from PyQt6.QtWidgets import QApplication
from src.models.re_database import initialize_re_db
from src.services.re_service import REProductService
from src import constants

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication([])
    if not initialize_re_db():
        print("ERROR init db")
        exit()
    payload = {
        "pid": "unique_pid_123467",
        "status_id": 1,
        "option_id": 1,
        "ward_id": 1,
        "street": "Main Street",
        "category_id": 1,
        "area": 100.5,
        "price": 250000.00,
        "legal_id": 1,
        "province_id": 1,
        "district_id": 1,
        "structure": 2,
        "function": "Residential",
        "building_line_id": 1,
        "furniture_id": 1,
        "description": "A lovely property",
        "image_paths": [
            "/Users/ndb/Downloads/z6468331727987_99497b4997d45dcd234add7924007ce6.jpg",
            "/Users/ndb/Downloads/z6468331728056_d359338fe0c87ed78259ebced92bbf5f.jpg",
            "/Users/ndb/Downloads/z6468331728057_0b21924c8eb3060d82d372c38c6c0c81.jpg",
            "/Users/ndb/Downloads/z6468331728058_57e38d5d902dc678f4e6e86977de5cbe.jpg",
            "/Users/ndb/Downloads/z6468331728059_76850a8b4b93e33237f5bf0049bdd03e.jpg",
            "/Users/ndb/Downloads/z6468331728060_6e1b2fcc19f59b745c1e70b45f2098bc.jpg",
            "/Users/ndb/Downloads/z6468331728213_c3cf48e153f4c4b701f6f49cfdc9e57a.jpg",
        ],
    }
    REProductService.create(payload)
    # REProductService.update(1, {"ward_id": 2})

    print(REProductService.read_all())
