# src/services/user_service.py
import os
from fake_useragent import UserAgent
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from src.services import service_utils
from src import constants


class BaseSettingService:
    TABLE_NAME = None  # To be overridden by subclasses

    @classmethod
    def _get_table_name(cls):
        if cls.TABLE_NAME is None:
            raise NotImplementedError(f"{cls.__name__} must define TABLE_NAME")
        return cls.TABLE_NAME

    @classmethod
    def create(cls, payload):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            columns = ", ".join(
                [
                    column
                    for column in payload.keys()
                    if column in BaseSettingService.get_columns(table_name)
                ]
            )
            placeholders = ", ".join(
                [
                    f":{key}"
                    for key in payload.keys()
                    if key in BaseSettingService.get_columns(table_name)
                ]
            )
            sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False

            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @classmethod
    def read(cls, record_id):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
        SELECT *
        FROM {table_name}
        WHERE id = :id
        """
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return False
        query.bindValue(":id", record_id)
        if not service_utils.exec_query(db, query):
            return None
        if query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            return row
        return None

    @classmethod
    def read_all(cls):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
        SELECT *
        FROM {table_name}
        """
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return False
        if not service_utils.exec_query(db, query):
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results

    @classmethod
    def update(cls, record_id, payload):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            sql_parts = []
            columns = BaseSettingService.get_columns(table_name)
            for key in columns:
                if key != "id" and key in payload:
                    sql_parts.append(f"{key}=:{key}")
            sql = f"""
            UPDATE {table_name}
            SET {", ".join(sql_parts)}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            WHERE id=:id
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            for key, value in payload.items():
                if key != "id":
                    query.bindValue(f":{key}", value)
            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @staticmethod
    def get_columns(table_name):
        db = QSqlDatabase.database("user_connection")
        record = db.record(table_name)
        if record.isEmpty():
            print(f"Table {table_name} does not exist.")
            return False
        columns = []
        for i in range(record.count()):
            field_name = record.fieldName(i)
            columns.append(field_name)
        return columns

    @classmethod
    def delete(cls, record_id):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            sql = f"""
            DELETE FROM {table_name}
            WHERE id=:id
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @classmethod
    def delete_multiple(cls, record_ids):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            if not record_ids:
                return True  # Không có ID nào để xóa
            placeholders = ", ".join("?" * len(record_ids))
            sql = f"""
            DELETE FROM {table_name}
            WHERE id IN ({placeholders})
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            for i, record_id in enumerate(record_ids):
                query.bindValue(i, record_id)

            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False


class UserService:
    @staticmethod
    def read(record_id):
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
SELECT *
FROM {constants.USER_TABLE}
WHERE id = {record_id}
"""
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return False
        if not service_utils.exec_query(db, query):
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
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
SELECT *
FROM {constants.USER_TABLE}
"""
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return []
        if not service_utils.exec_query(db, query):
            return []
        results = []
        while query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = record.value(i)
                data[field_name] = field_value
            results.append(data)
        return results

    @staticmethod
    def create(payload):
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        ua_desktop_controller = UserAgent(
            os="Mac OS X",)
        ua_mobile_controller = UserAgent(
            os="iOS",)
        payload.setdefault("mobile_ua", ua_mobile_controller.random)
        payload.setdefault("desktop_ua", ua_desktop_controller.random)
        query = QSqlQuery(db)
        try:
            columns = ", ".join(
                [
                    column
                    for column in payload.keys()
                    if column in get_columns(constants.USER_TABLE)
                ]
            )
            placeholders = ", ".join(
                [
                    f":{key}"
                    for key in payload.keys()
                    if key in get_columns(constants.USER_TABLE)
                ]
            )
            sql = f"""
            INSERT INTO {constants.USER_TABLE} ({columns})
            VALUES ({placeholders})
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @staticmethod
    def update(record_id, payload):
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            sql_parts = []
            columns = get_columns(constants.USER_TABLE)
            for key in columns:
                if key != "id":
                    if key in payload.keys():
                        sql_parts.append(f"{key}=:{key}")
            sql = f"""
            UPDATE {constants.USER_TABLE}
            SET {", ".join(sql_parts)}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            WHERE id=:id
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            for key in columns:
                if key != "id":
                    if key in payload.keys():
                        query.bindValue(f":{key}", payload.get(key))
            query.bindValue(":id", record_id)
            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @staticmethod
    def delete(record_id):
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
        query = QSqlQuery(db)
        try:
            sql = f"""
            DELETE FROM {constants.USER_TABLE}
            WHERE id=:id
            """
            query = QSqlQuery(db)
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            query.bindValue(":id", record_id)
            user_data_dir = UserDataDirService.get_selected_data_dir()
            if not service_utils.delete_dir(os.path.join(user_data_dir, str(id))):
                db.rollback()
                return False
            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False

    @staticmethod
    def delete_multiple(record_ids):
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        query = QSqlQuery(db)
        try:
            if not record_ids:
                return True  # Không có ID nào để xóa
            placeholders = ", ".join("?" * len(record_ids))
            sql = f"""
            DELETE FROM {constants.USER_TABLE}
            WHERE id IN ({placeholders})
            """
            if not query.prepare(sql):
                service_utils.error(query.lastError().text())
                return False
            for i, record_id in enumerate(record_ids):
                query.bindValue(i, record_id)

            user_data_dir = UserDataDirService.get_selected_data_dir()

            for id in record_ids:
                if not service_utils.delete_dir(os.path.join(user_data_dir, str(id))):
                    db.rollback()
                    return False

            if not service_utils.exec_query(db, query):
                return False
            service_utils.is_affected(query)
            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False


class UserDataDirService(BaseSettingService):
    TABLE_NAME = constants.USER_SETTING_USER_DATA_DIR_TABLE

    @classmethod
    def get_selected_data_dir(cls):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
        SELECT value
        FROM {table_name}
        WHERE is_selected = 1
        """
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return False
        if not service_utils.exec_query(db, query):
            return None
        if query.next():
            return query.value(0)
        return None

    @classmethod
    def set_selected_data_dir(cls, record_id):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        if not db.transaction():
            service_utils.error("Failed to start transaction.")
            return False
        try:
            # Unselect all first
            unselect_query = QSqlQuery(db)
            unselect_sql = f"""
            UPDATE {table_name}
            SET is_selected = 0
            """
            if not unselect_query.exec(unselect_sql):
                service_utils.error(unselect_query.lastError().text())
                db.rollback()
                return False

            # Select the new one
            select_query = QSqlQuery(db)
            select_sql = f"""
            UPDATE {table_name}
            SET is_selected = 1
            WHERE id = :id
            """
            if not select_query.prepare(select_sql):
                service_utils.error(select_query.lastError().text())
                db.rollback()
                return False
            select_query.bindValue(":id", record_id)
            if not select_query.exec():
                service_utils.error(select_query.lastError().text())
                db.rollback()
                return False

            if not service_utils.commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            service_utils.error(f"ERROR: {e}")
            return False


class UserProxyService(BaseSettingService):
    TABLE_NAME = constants.USER_SETTING_PROXY_TABLE

    @classmethod
    def is_value_existed(cls, value):
        table_name = cls._get_table_name()
        db = QSqlDatabase.database("user_connection")
        query = QSqlQuery(db)
        sql = f"""
        SELECT 1
        FROM {table_name}
        WHERE value = :value
        """
        if not query.prepare(sql):
            service_utils.error(query.lastError().text())
            return False
        query.bindValue(":value", value)
        if not query.exec():
            service_utils.error(query.lastError().text())
            return False
        return query.next()
