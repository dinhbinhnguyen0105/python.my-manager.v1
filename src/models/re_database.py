# src/models/re_database.py
import logging
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src import constants

logger = logging.getLogger(__name__)


def initialize_re_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(constants.PATH_DB)
    if not db.open():
        logger.error(f"Error opening database: {db.lastError().text()}")
        return False
    query = QSqlQuery(db)
    query.exec("PRAGMA foreign_keys = ON;")
    try:
        if not db.transaction():
            logger.error("Could not start transaction.")
            return False

        if not _create_tables(db):
            db.rollback()
            return False
        if not _seed_data_s(db):
            db.rollback()
            return False

        if not db.commit():
            logger.error("Commit failed")
            return False
        return True
    except Exception as e:
        if db.isOpen():
            db.rollback()
        logger.error(
            f"Database initialization failed: {str(e)}", exc_info=True)
        return False


def _create_tables(db: QSqlDatabase):
    for table in [
        constants.RE_SETTING_STATUSES_TABLE,
        constants.RE_SETTING_PROVINCES_TABLE,
        constants.RE_SETTING_DISTRICTS_TABLE,
        constants.RE_SETTING_WARDS_TABLE,
        constants.RE_SETTING_OPTIONS_TABLE,
        constants.RE_SETTING_CATEGORIES_TABLE,
        constants.RE_SETTING_BUILDING_LINE_S_TABLE,
        constants.RE_SETTING_FURNITURE_S_TABLE,
        constants.RE_SETTING_LEGAL_S_TABLE,
    ]:
        if not _create_dep_table(db, table):
            return False
    if not _create_product_table(db):
        return False
    if not _create_template_table(db):
        return False
    if not _create_img_dir_table(db):
        return False
    return True


def _seed_data_s(db: QSqlDatabase):
    if not _seed_dep(
        db, constants.RE_SETTING_STATUSES_TABLE, constants.RE_SETTING_STATUSES
    ):

        return False
    if not _seed_dep(
        db, constants.RE_SETTING_PROVINCES_TABLE, constants.RE_SETTING_PROVINCES
    ):
        return False
    if not _seed_dep(
        db, constants.RE_SETTING_DISTRICTS_TABLE, constants.RE_SETTING_DISTRICTS
    ):
        return False
    if not _seed_dep(db, constants.RE_SETTING_WARDS_TABLE, constants.RE_SETTING_WARDS):
        return False
    if not _seed_dep(
        db, constants.RE_SETTING_OPTIONS_TABLE, constants.RE_SETTING_OPTIONS
    ):
        return False
    if not _seed_dep(
        db, constants.RE_SETTING_CATEGORIES_TABLE, constants.RE_SETTING_CATEGORIES
    ):
        return False
    if not _seed_dep(
        db,
        constants.RE_SETTING_BUILDING_LINE_S_TABLE,
        constants.RE_SETTING_BUILDING_LINE_S,
    ):
        return False
    if not _seed_dep(
        db, constants.RE_SETTING_FURNITURE_S_TABLE, constants.RE_SETTING_FURNITURE_S
    ):
        return False
    if not _seed_dep(
        db, constants.RE_SETTING_LEGAL_S_TABLE, constants.RE_SETTING_LEGAL_S
    ):
        return False
    if not _seed_title_template(db):
        return False
    if not _seed_description_template(db):
        return False
    if not _seed_dir_img(db):
        return False
    return True


def _create_product_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {constants.RE_PRODUCT_TABLE} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
pid TEXT UNIQUE NOT NULL,
status_id INTEGER,
option_id INTEGER,
ward_id INTEGER,
street TEXT,
category_id INTEGER,
area REAL,
price REAL,
legal_id INTEGER,
province_id INTEGER,
district_id INTEGER,
structure REAL,
function TEXT,
building_line_id INTEGER,
furniture_id INTEGER,
description TEXT,
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
FOREIGN KEY (status_id) REFERENCES {constants.RE_SETTING_STATUSES_TABLE}(id),
FOREIGN KEY (province_id) REFERENCES {constants.RE_SETTING_PROVINCES_TABLE}(id),
FOREIGN KEY (district_id) REFERENCES {constants.RE_SETTING_DISTRICTS_TABLE}(id),
FOREIGN KEY (ward_id) REFERENCES {constants.RE_SETTING_WARDS_TABLE}(id),
FOREIGN KEY (option_id) REFERENCES {constants.RE_SETTING_OPTIONS_TABLE}(id),
FOREIGN KEY (category_id) REFERENCES {constants.RE_SETTING_CATEGORIES_TABLE}(id),
FOREIGN KEY (building_line_id) REFERENCES {constants.RE_SETTING_BUILDING_LINE_S_TABLE}(id),
FOREIGN KEY (furniture_id) REFERENCES {constants.RE_SETTING_FURNITURE_S_TABLE}(id),
FOREIGN KEY (legal_id) REFERENCES {constants.RE_SETTING_LEGAL_S_TABLE}(id)
)
"""
    if not query.exec(sql):
        logger.error(
            f"Error creating table '{constants.RE_PRODUCT_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _create_template_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    for table_name in [
        constants.RE_TEMPLATE_TITLE_TABLE,
        constants.RE_TEMPLATE_DESCRIPTION_TABLE,
    ]:
        sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tid TEXT UNIQUE,
    option_id INTEGER,
    value TEXT,
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (option_id) REFERENCES {constants.RE_SETTING_OPTIONS_TABLE}(id)
)
"""
        if not query.exec(sql):
            logger.error(
                f"Error creating table '{table_name}': {query.lastError().text()}"
            )
            return False
    return True


def _create_dep_table(db: QSqlDatabase, table_name):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
label_vi TEXT,
label_en TEXT,
value TEXT UNIQUE NOT NULL,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
    if not query.exec(sql):
        logger.error(
            f"Error creating table '{table_name}': {query.lastError().text()}")
        return False
    return True


def _create_img_dir_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {constants.RE_SETTING_IMG_DIR_TABLE} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value TEXT UNIQUE NOT NULL,
is_selected INTEGER,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
    if not query.exec(sql):
        logger.error(
            f"Error creating table '{constants.RE_SETTING_IMG_DIR_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _seed_dir_img(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
INSERT OR IGNORE INTO {constants.RE_SETTING_IMG_DIR_TABLE} (id, value, is_selected)
VALUES(0, "{constants.RE_SETTING_IMG_DIR[0].get("value")}", 1)
"""
    if not query.exec(sql):
        logger.error(
            f"Error seeding table '{constants.RE_SETTING_IMG_DIR_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _seed_title_template(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
INSERT OR IGNORE INTO {constants.RE_TEMPLATE_TITLE_TABLE} (id, tid, option_id, value)
VALUES (:id, :tid, :option_id, :value)
"""
    if not query.prepare(sql):
        logger.error(query.lastError().text())
        return False
    query.bindValue(":id", 0)
    query.bindValue(":tid", "T.T.default")
    query.bindValue(":option_id", 1)
    query.bindValue(
        ":value",
        "[<option>] <icon><icon> cần <option> <category> <price> <unit>, <ward>, <district>, <province> <icon><icon>",
    )
    if not query.exec():
        logger.error(
            f"Error seeding table '{constants.RE_TEMPLATE_TITLE_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _seed_description_template(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
INSERT OR IGNORE INTO {constants.RE_TEMPLATE_DESCRIPTION_TABLE} (id, tid, option_id, value)
VALUES (:id, :tid, :option_id, :value)
"""
    if not query.prepare(sql):
        logger.error(query.lastError().text())
        return False
    query.bindValue(":id", 0)
    query.bindValue(":tid", "T.D.default")
    query.bindValue(":option_id", 1)
    query.bindValue(
        ":value",
        "ID: <PID>\n🗺 Vị trí: đường <street>, <ward>, <district>\n📏 Diện tích: <area>\n🏗 Kết cấu: <structure>\n🛌 Công năng: <function>\n📺 Nội thất: <furniture>\n🚗 Lộ giới: <building_line>\n📜 Pháp lý: <legal>\n<icon><icon> Mô tả:\n<description>\n------------\n💵 Giá: <price><unit>- Thương lượng chính chủ\n\n☎ Liên hệ: 0375.155.525 - Mr. Bình\n🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺\n🌺Ký gửi mua, bán - cho thuê, thuê bất động sản xin liên hệ 0375.155.525 - Mr. Bình🌺\n🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺",
    )
    if not query.exec():
        logger.error(
            f"Error seeding table '{constants.RE_TEMPLATE_DESCRIPTION_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _seed_dep(db: QSqlDatabase, table_name, payload):
    query = QSqlQuery(db)
    sql = f"""
INSERT OR IGNORE INTO {table_name} (id, label_vi, label_en, value)
VALUES (:id, :label_vi, :label_en, :value)
"""
    if not query.prepare(sql):
        logger.error(query.lastError().text())
        return False
    for index, field in enumerate(payload):
        query.bindValue(":id", index)
        query.bindValue(":label_vi", field.get("label_vi", ""))
        query.bindValue(":label_en", field.get("label_en", ""))
        query.bindValue(":value", field.get("value", ""))
        if not query.exec():
            logger.error(
                f"Error inserting into '{table_name}': {query.lastError().text()}"
            )
            return False
    return True
