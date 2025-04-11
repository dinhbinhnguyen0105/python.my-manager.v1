# src/services/re_service.py
import logging
import os
from PyQt6.QtSql import QSqlQuery, QSqlDatabase

from src import constants
from .re_service_utils import (
    exec_query,
    commit_db,
    is_affected,
    get_columns,
    copy_files,
    is_value_existed,
)

logger = logging.getLogger(__name__)


class REProductService:
    @staticmethod
    def read(record_id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
SELECT 
main.id,
main.pid,
main.street,
main.area,
main.structure,
main.function,
main.description,
main.price,
main.updated_at,
statuses.label_vi AS status,
provinces.label_vi AS province,
districts.label_vi AS district,
wards.label_vi AS ward,
options.label_vi AS option,
categories.label_vi AS category,
building_line_s.label_vi AS building_line,
furniture_s.label_vi AS furniture,
legal_s.label_vi AS legal
FROM {constants.RE_PRODUCT_TABLE} main
JOIN {constants.RE_SETTING_STATUSES_TABLE} statuses ON main.status_id = statuses.id
JOIN {constants.RE_SETTING_PROVINCES_TABLE} provinces ON main.province_id = provinces.id
JOIN {constants.RE_SETTING_DISTRICTS_TABLE} districts ON main.district_id = districts.id
JOIN {constants.RE_SETTING_WARDS_TABLE} wards ON main.ward_id = wards.id
JOIN {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
JOIN {constants.RE_SETTING_CATEGORIES_TABLE} categories ON main.category_id = categories.id
JOIN {constants.RE_SETTING_BUILDING_LINE_S_TABLE} building_line_s ON main.building_line_id = building_line_s.id
JOIN {constants.RE_SETTING_FURNITURE_S_TABLE} furniture_s ON main.furniture_id = furniture_s.id
JOIN {constants.RE_SETTING_LEGAL_S_TABLE} legal_s ON main.legal_id = legal_s.id
WHERE main.id=:id
"""
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        query.bindValue(":id", record_id)
        if not exec_query(db, query):
            return None
        if query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = record.value(i)
                data[field_name] = field_value
            return data
        return None

    @staticmethod
    def read_all():
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
SELECT 
main.id,
main.pid,
main.street,
main.area,
main.structure,
main.function,
main.description,
main.price,
main.updated_at,
statuses.label_vi AS status,
provinces.label_vi AS province,
districts.label_vi AS district,
wards.label_vi AS ward,
options.label_vi AS option,
categories.label_vi AS category,
building_line_s.label_vi AS building_line,
furniture_s.label_vi AS furniture,
legal_s.label_vi AS legal
FROM {constants.RE_PRODUCT_TABLE} main
JOIN {constants.RE_SETTING_STATUSES_TABLE} statuses ON main.status_id = statuses.id
JOIN {constants.RE_SETTING_PROVINCES_TABLE} provinces ON main.province_id = provinces.id
JOIN {constants.RE_SETTING_DISTRICTS_TABLE} districts ON main.district_id = districts.id
JOIN {constants.RE_SETTING_WARDS_TABLE} wards ON main.ward_id = wards.id
JOIN {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
JOIN {constants.RE_SETTING_CATEGORIES_TABLE} categories ON main.category_id = categories.id
JOIN {constants.RE_SETTING_BUILDING_LINE_S_TABLE} building_line_s ON main.building_line_id = building_line_s.id
JOIN {constants.RE_SETTING_FURNITURE_S_TABLE} furniture_s ON main.furniture_id = furniture_s.id
JOIN {constants.RE_SETTING_LEGAL_S_TABLE} legal_s ON main.legal_id = legal_s.id
"""
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        if not exec_query(db, query):
            return None
        results = []
        while query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = query.value(i)
                data[field_name] = field_value
            results.append(data)
        return results

    @staticmethod
    def create(payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
        query = QSqlQuery(db)
        try:
            columns = ", ".join(
                [
                    column
                    for column in payload.keys()
                    if column in get_columns(constants.RE_PRODUCT_TABLE)
                ]
            )
            placeholders = ", ".join(
                [
                    f":{key}"
                    for key in payload.keys()
                    if key in get_columns(constants.RE_PRODUCT_TABLE)
                ]
            )
            sql = f"""
            INSERT INTO {constants.RE_PRODUCT_TABLE} ({columns})
            VALUES ({placeholders})
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False

            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            img_record = REImageDirService.read({"is_selected": 1})
            if not img_record:
                db.rollback()
                logger.error("Image dir path is undefined.")
                return False

            if not exec_query(db, query):
                return False
            is_affected(query)
            image_paths = payload.get("image_paths")

            current_id = None
            current_id_query = QSqlQuery(db)
            if current_id_query.exec("SELECT last_insert_rowid();"):
                if current_id_query.next():
                    current_id = current_id_query.value(0)
            else:
                db.rollback()
                logger.error(
                    f"Error get the ID of the latest record: {current_id_query.lastError().text()}"
                )
                return False
            image_dir = os.path.join(img_record.get("value"), str(current_id))
            if not copy_files(image_paths, image_dir, current_id):
                db.rollback()
                return False
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def update(record_id, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
        query = QSqlQuery(db)
        try:
            sql_parts = []
            columns = get_columns(constants.RE_PRODUCT_TABLE)
            for key in columns:
                if key != "id":
                    if key in payload.keys():
                        sql_parts.append(f"{key}=:{key}")
            sql = f"""
            UPDATE {constants.RE_PRODUCT_TABLE}
            SET {", ".join(sql_parts)}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            WHERE id=:id
            """
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            for key in columns:
                if key != "id":
                    if key in payload.keys():
                        query.bindValue(f":{key}", payload.get(key))
            query.bindValue(":id", record_id)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def delete(record_id):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
        query = QSqlQuery(db)
        try:
            sql = f"""
            DELETE FROM {constants.RE_PRODUCT_TABLE}
            WHERE id=:id
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def is_pid_existed(pid):
        return is_value_existed(constants.RE_PRODUCT_TABLE, {"pid": pid})


class RESettingService:
    @staticmethod
    def read(table_name, record_id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT id, label_vi, label_en, value, updated_at
        FROM {table_name}
        WHERE id = :id
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        query.bindValue(":id", record_id)
        if not exec_query(db, query):
            return None
        if query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            return row
        return None

    @staticmethod
    def read_all(table_name):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT id, label_vi, label_en, value, updated_at
        FROM {table_name}
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        if not exec_query(db, query):
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results

    @staticmethod
    def create(table_name, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            columns = ", ".join(payload.keys())
            placeholders = ", ".join([f":{key}" for key in payload.keys()])
            sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def update(table_name, record_id, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            sql_parts = []
            for key, value in payload.items():
                if key != "id":
                    sql_parts.append(f"{key}=:{key}")
            sql = f"""
            UPDATE {table_name}
            SET {", ".join(sql_parts)}
            WHERE id=:id
            """
            payload["id"] = record_id
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def delete(table_name, record_id):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            sql = f"""
            DELETE FROM {table_name}
            WHERE id=:id
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False


class RETemplateService:
    @staticmethod
    def read(table_name, id, language="vi"):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT 
            main.id AS id,
            main.tid AS tid,
            options.id AS option_id,
            {"options.label_vi AS option_label" if language == "vi" else "options.label_en AS option_label"},
            options.value AS option_value,
            main.value AS value,
            main.updated_at AS updated_at
        FROM {table_name} main
        JOIN  {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
        WHERE main.id = :id
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        query.bindValue(":id", id)
        if not exec_query(db, query):
            return None
        if query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            return row
        return None

    @staticmethod
    def read_all(table_name, language="vi"):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT 
            main.id AS id,
            main.tid AS tid,
            options.id AS option_id,
            {"options.label_vi AS option_label" if language == "vi" else "options.label_en AS option_label"},
            options.value AS option_value,
            main.value AS value,
            main.updated_at AS updated_at
        FROM {table_name} main
        JOIN {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        if not exec_query(db, query):
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results

    @staticmethod
    def create(table_name, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            sql = f"""
            INSERT INTO {table_name} (tid, option_id, value)
            VALUES (:tid, :option_id, :value)
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def update(table_name, id, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            set_clause = ", ".join(
                [f"{key} = :{key}" for key in payload.keys()])
            sql = f"""
            UPDATE {table_name}
            SET {set_clause}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            WHERE id = :id
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", id)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def delete(table_name, id):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            query = QSqlQuery(db)
            sql = f"""
            DELETE FROM {table_name} WHERE id = :id
            """
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", id)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False


class REImageDirService:
    @staticmethod
    def read(condition):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT 
            id, value, is_selected, updated_at
        FROM {constants.RE_SETTING_IMG_DIR_TABLE}
        WHERE {list(condition.keys())[0]} = {list(condition.values())[0]}
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        # query.bindValue(":id", condition)
        if not exec_query(db, query):
            return None
        if query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            return row
        return None

    @staticmethod
    def read_all():
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
        SELECT 
            id, value, is_selected, updated_at
        FROM {constants.RE_SETTING_IMG_DIR_TABLE}
        """
        if not query.prepare(sql):
            logger.error(query.lastError().text())
            return False
        if not exec_query(db, query):
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results

    @staticmethod
    def create(payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            sql = f"""
            INSERT INTO {constants.RE_SETTING_IMG_DIR_TABLE} (value, is_selected)
            VALUES (:value, :is_selected)
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def update(id, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            set_clause = ", ".join(
                [f"{key} = :{key}" for key in payload.keys()])
            sql = f"""
            UPDATE {constants.RE_SETTING_IMG_DIR_TABLE}
            SET {set_clause}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            WHERE id = :id
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", id)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def delete(record_id):
        db = QSqlDatabase.database()
        if not db.transaction():
            logger.error("Failed to start transaction.")
            return False
        try:
            query = QSqlQuery(db)
            sql = f"""
            DELETE FROM {constants.RE_SETTING_IMG_DIR_TABLE} WHERE id = :id
            """
            if not query.prepare(sql):
                logger.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            if not exec_query(db, query):
                return False
            is_affected(query)
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False
