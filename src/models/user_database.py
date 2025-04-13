# src/models/user_database.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src import constants
from src.utils.logger import error


def initialize_user_db():
    db = QSqlDatabase.addDatabase("QSQLITE", "user_connection")
    db.setDatabaseName(constants.PATH_USER_DB)
    if not db.open():
        error(f"Error opening database: {db.lastError().text()}")
        return False
    query = QSqlQuery(db)
    query.exec("PRAGMA foreign_keys = ON;")

    try:
        if not db.transaction():
            error("Could not start transaction.")
            return False
        if not _create_user_table(db):
            return False
        if not _create_user_setting_udd_table(db):
            return False
        if not _create_user_setting_proxy_table(db):
            return False
        if not _seed_user_data_dir(db):
            return False
        if not db.commit():
            error("[initialize_user_db] Commit false")
        return True
    except Exception as e:
        if db.isOpen():
            db.rollback()
        error(
            f"Database initialization failed: {str(e)}")
        return False


def _create_user_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {constants.USER_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status INTEGER,
    uid TEXT,
    username TEXT,
    password TEXT,
    two_fa TEXT,
    email TEXT,
    email_password TEXT,
    phone_number TEXT,
    note TEXT,
    type TEXT,
    user_group TEXT,
    mobile_ua TEXT,
    desktop_ua TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
    if not query.exec(sql):
        error(
            f"Error creating table '{constants.USER_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _create_user_setting_udd_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {constants.USER_SETTING_USER_DATA_DIR_TABLE} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value TEXT UNIQUE NOT NULL,
is_selected INTEGER,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
    if not query.exec(sql):
        error(
            f"Error creating table '{constants.USER_SETTING_USER_DATA_DIR_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _create_user_setting_proxy_table(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
CREATE TABLE IF NOT EXISTS {constants.USER_SETTING_PROXY_TABLE} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value TEXT UNIQUE NOT NULL,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
    if not query.exec(sql):
        error(
            f"Error creating table '{constants.USER_SETTING_PROXY_TABLE}': {query.lastError().text()}"
        )
        return False
    return True


def _seed_user_data_dir(db: QSqlDatabase):
    query = QSqlQuery(db)
    sql = f"""
INSERT OR IGNORE INTO {constants.USER_SETTING_USER_DATA_DIR_TABLE} (id, value, is_selected)
VALUES(0, "{constants.USER_SETTING_USER_DATA_DIR[0].get("value")}", 1)
"""
    if not query.exec(sql):
        error(
            f"Error seeding table '{constants.USER_SETTING_USER_DATA_DIR_TABLE}': {query.lastError().text()}"
        )
        return False
    return True
