# src/models/products_database.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src.contants import REAL_ESTATE_PRODUCT_TABLE, REAL_ESTATE_TEMPLATE_TABLE


def initialize_products_database() -> bool:
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("./src/data/real_estate.db")
    if not db.open():
        return False
    query = QSqlQuery()
    query.exec(f"""
CREATE TABLE IF NOT EXISTS {REAL_ESTATE_PRODUCT_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pid TEXT UNIQUE NOT NULL,
                province_name TEXT,
                district_name TEXT,
                ward_name TEXT,
                street_name TEXT,
                category TEXT,
                option TEXT,
                area REAL,
                structure REAL,
                function TEXT,
                furniture TEXT,
                building_line TEXT,
                legal REAL,
                description TEXT,
                price REAL,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updated_at TEXT
               )
    """)

    return True
