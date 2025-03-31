# src/models/database.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def initialize_user_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("./src/data/user.db")
    if not db.open():
        return False
    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS users_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                uid TEXT,
                password TEXT NOT NULL,
                twoFA TEXT,
                email TEXT,
                emailPassword TEXT,
                phoneNumber TEXT,
                group TEXT,
                type TEXT,
                note TEXT,
                status INTEGER DEFAULT 1,
                createdAt TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updatedAt TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
               )
    """)
    query.exec("""
               CREATE TABLE IF NOT EXISTS user_browsers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mobile_userAgent TEXT NOT NULL,
                mobile_screenHeight INTEGER NOT NULL,
                mobile_screenWidth INTEGER NOT NULL,
                mobile_viewportHeight INTEGER NOT NULL,
                mobile_viewportWidth INTEGER NOT NULL,
                desktop_userAgent TEXT NOT NULL,
                desktop_viewportHeight INTEGER NOT NULL,
                desktop_viewportWidth INTEGER NOT NULL,
                desktop_screenHeight INTEGER NOT NULL,
                desktop_screenWidth INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users_info(id) ON DELETE CASCADE
               )
    """)
    query.exec("""
               CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                browser_id INTEGER,
                is_selected INTEGER DEFAULT 0
                FOREIGN KEY (user_id) REFERENCES users_info(id) ON DELETE CASCADE,
                FOREIGN KEY (browser_id) REFERENCES user_browsers(id) ON DELETE SET NULL
               )
    """)

    return True


def initialize_product_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("./src/data/product.db")
    if not db.open():
        return False
    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_options (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    options = ["rent", "sell", "assignment"]
    for option in options:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_options (name) VALUES (?)")
        query.addBindValue(option)
        if not query.exec():
            raise Exception(
                f"[ERROR] add option '{option}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_categories (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    categories = ["house", "shop_house", "villa", "apartment", "hotel",
                  "homestay", "land", "retail space", "workshop", "coffee house", ]
    for category in categories:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_categories (name) VALUES (?)")
        query.addBindValue(category)
        if not query.exec():
            raise Exception(
                f"[ERROR] add category '{category}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_structures (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_provinces (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)

    provinces = ["lamdong"]
    for province in provinces:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_provinces (name) VALUES (?)")
        query.addBindValue(province)
        if not query.exec():
            raise Exception(
                f"[ERROR] add province '{province}': {query.lastError().text()}")
    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_districts (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    districts = ["dalat"]
    for district in districts:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_districts (name) VALUES (?)")
        query.addBindValue(district)
        if not query.exec():
            raise Exception(
                f"[ERROR] add district '{district}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_wards (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    wards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "11", "12", "tanung", "tramhanh", "xuantruong", "xuantho",]
    for ward in wards:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_wards (name) VALUES (?)")
        query.addBindValue(ward)
        if not query.exec():
            raise Exception(
                f"[ERROR] add ward '{ward}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_furniture (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    furniture_s = ["basic", "full", "none"]
    for furniture in furniture_s:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_furniture (name) VALUES (?)")
        query.addBindValue(furniture)
        if not query.exec():
            raise Exception(
                f"[ERROR] add furniture '{furniture}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_building_line (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    building_line_s = ["motorbike", "car"]
    for building_line in building_line_s:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_building_line (name) VALUES (?)")
        query.addBindValue(building_line)
        if not query.exec():
            raise Exception(
                f"[ERROR] add building_line '{building_line}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate_legal (
               id INTEGER PRIMARY KEY AUTOINCREMENT
               name TEXT UNIQUE NOT NULL
               )
               """)
    legal_s = ["khongso", "sonongnghiepchung", "sonongnghiepphanquyen",
               "sononnghieprieng", "soxaydungchung", "soxaydungphanquyen", "soxaydungrieng", ]
    for legal in legal_s:
        query.prepare(
            "INSERT OR IGNORE INTO real_estate_legal (name) VALUES (?)")
        query.addBindValue(legal)
        if not query.exec():
            raise Exception(
                f"[ERROR] add legal '{legal}': {query.lastError().text()}")

    query.exec("""
               CREATE TABLE IF NOT EXISTS real_estate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pid TEXT UNIQUE NOT NULL,
                option_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                province_id INTEGER NOT NULL,
                district_id INTEGER NOT NULL,
                ward_id INTEGER NOT NULL,
                furniture_id INTEGER NOT NULL,
                legal_id INTEGER NOT NULL,
                street TEXT,
                area INTEGER NOT NULL,
                structure TEXT,
                function TEXT,
                building_line INTEGER NOT NULL,
                price REAL,
                description TEXT,
                status INTEGER DEFAULT 1,
                createdAt TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updatedAt TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
               
                FOREIGN KEY (option_id) REFERENCES real_estate_options(id),
                FOREIGN KEY (category_id) REFERENCES real_estate_categories(id),
                FOREIGN KEY (province_id) REFERENCES real_estate_provinces(id),
                FOREIGN KEY (district_id) REFERENCES real_estate_districts(id),
                FOREIGN KEY (ward_id) REFERENCES real_estate_wards(id),
                FOREIGN KEY (furniture_id) REFERENCES real_estate_furniture(id),
                FOREIGN KEY (legal_id) REFERENCES real_estate_legal(id),
                FOREIGN KEY (building_line) REFERENCES real_estate_building_line(id)
               )
               """)
    return True
