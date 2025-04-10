# src/services/re_service_utils.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import logging, os, shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def commit_db(db):
    if not db.commit():
        logger.error("Failed to commit transaction.")
        return False
    return True


def exec_query(db, query):
    sql = query.lastQuery()
    if not query.exec():
        print("Query bound names:", query.boundValues())
        logger.error(
            f"Error executing SQL query: {sql}\nERROR message: {query.lastError().text()}"
        )
        db.rollback()
        return False
    return True


def is_affected(query):
    rows_affected = query.numRowsAffected()
    if rows_affected > 0:
        print(f"Updated {rows_affected} record(s).")
        return True
    else:
        sql = query.lastQuery()
        print(f"No records were updated.")
        print(sql)
        return False


def is_value_existed(table_name, condition):
    db = QSqlDatabase.database()
    query = QSqlQuery(db)
    sql = f"""
SELECT COUNT(*) FROM {table_name}
WHERE {list(condition.keys())[0]} = :{list(condition.values())[0]}
"""
    if not query.prepare(sql):
        logger.error(query.lastError().text())
        return False
    if not exec_query(db, query):
        return False
    if query.next():
        return query.value(0) > 0
    return False


def get_columns(table_name):
    db = QSqlDatabase.database()
    record = db.record(table_name)
    if record.isEmpty():
        print(f"Table {table_name} does not exist.")
        return False
    columns = []
    for i in range(record.count()):
        field_name = record.fieldName(i)
        columns.append(field_name)
    return columns


def get_ids(table_name, condition=None):
    db = QSqlDatabase.database()
    query = QSqlQuery(db)
    if not condition:
        sql = f"""
SELECT id FROM {table_name}
"""
    else:
        sql = f"""
SELECT id FROM {table_name} WHERE {list(condition.keys())[0]} = {list(condition.values())[0]}
"""
    if not query.prepare(sql):
        logger.error(query.lastError().text())
        return False
    if not exec_query(db, query):
        return []
    ids = []
    while query.next():
        ids.append(query.value(0))
    return ids


def copy_files(sources, destination, id):
    os.makedirs(destination, exist_ok=True)
    destination_img_num = len(get_images_in_directory(destination))

    for index, file in enumerate(sources):
        _, extension = os.path.splitext(file)
        file_name = f"{id}_{index + destination_img_num}{extension}"
        destination_path = os.path.join(destination, file_name)
        try:
            shutil.copy2(file, destination_path)
        except FileNotFoundError:
            print(f"Error: File not found: {file}")
            return False
        except Exception as e:
            print(f"Error copying {file}: {e}")
            return False
    return True


def get_images_in_directory(image_dir):
    if not os.path.exists(image_dir):
        return []
    images = []
    for file in os.listdir(image_dir):
        if file.endswith((".png", ".jpg", ".jpeg")):
            images.append(os.path.join(image_dir, file))
    return images
