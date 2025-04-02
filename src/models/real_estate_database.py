# src/models/products_database.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src.constants import REAL_ESTATE_PRODUCT_TABLE, REAL_ESTATE_TEMPLATE_TABLE


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
                province TEXT,
                district TEXT,
                ward TEXT,
                street TEXT,

                option TEXT,
                category TEXT,
                
                area REAL,
                structure REAL,
                function TEXT,
                furniture TEXT,
                building_line TEXT,
                legal TEXT,
                description TEXT,
                price REAL,
                status INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updated_at TEXT
               )
    """)

    return True
