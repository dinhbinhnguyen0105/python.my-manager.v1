# src/services/service_utils.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src.utils.logger import error, warning, info
import os
import shutil


def commit_db(db):
    if not db.commit():
        error("Failed to commit transaction.")
        return False
    return True


def exec_query(db, query):
    sql = query.lastQuery()
    if not query.exec():
        print("Query bound names:", query.boundValues())
        error(
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
        error(query.lastError().text())
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


def delete_dir(dir_path):
    dir_path = os.path.abspath(dir_path)
    if not os.path.exists(dir_path):
        warning(f"directory '{dir_path}' does not exist.".lower())
        return True
    try:
        shutil.rmtree(dir_path)
        info(f"successfully deleted directory: '{dir_path}'".lower())
        return True
    except OSError as e:
        error(f"error deleting directory '{dir_path}': {e}".lower())
        return False
