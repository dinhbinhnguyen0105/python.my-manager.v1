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


def initialize_products() -> bool:
    query = QSqlQuery()
    query.exec(f"""
               CREATE TABLE IF NOT EXISTS real_estate_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT
                pid TEXT UNIQUE NOT NULL,
                province_id INTEGER,
                district_id INTEGER,
                ward_id INTEGER,
                option_id INTEGER,
                category_id INTEGER,
                building_line_id INTEGER,
                furniture_id INTEGER,
                legal_id INTEGER,
                area REAL,
                structure REAL,
                function TEXT,
                description TEXT,
                price REAL,
                status INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updated_at TEXT,
                FOREIGN KEY (province_id) REFERENCES real_estate_options(id),
                FOREIGN KEY (district_id) REFERENCES real_estate_districts(id),
                FOREIGN KEY (ward_id) REFERENCES real_estate_wards(id),
                FOREIGN KEY (option_id) REFERENCES real_estate_options(id),
                FOREIGN KEY (category_id) REFERENCES real_estate_categories(id),
                FOREIGN KEY (building_line_id) REFERENCES real_estate_building_line_s(id),
                FOREIGN KEY (furniture_id) REFERENCES real_estate_furniture_s(id),
                FOREIGN KEY (legal_id) REFERENCES real_estate_legal_s(id),
               )
               """)


def initialize_deps(table_name: str, fields: dict) -> bool:
    query = QSqlQuery()
    query.exec(f"""CREATE TABLE IF NOT EXISTS {table_name} (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name_vi TEXT,
               name_en TEXT,
               value TEXT UNIQUE NOT NULL,
               )""")
    query.prepare(f"""
                  INSERT OR IGNORE {table_name}(name_vi, name_en, value)
                  VALUES (:name_vi, :name_en, :value)
                  """)
    for field in fields:
        query.bindValue(":name_vi", field.get("name_vi", ""))
        query.bindValue(":name_en", field.get("name_en", ""))
        query.bindValue(":value", field.get("value", ""))
        if not query.exec():
            if not query.exec():
                raise Exception(
                    f"Error inserting province '{table_name['value']}': {query.lastError().text()}")

    return True
