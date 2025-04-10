# src/services/re_service.py
import datetime
import os
import shutil
import logging
from PyQt6.QtSql import QSqlQuery, QSqlDatabase

from src import constants
from .re_service_utils import exec_query, commit_db

logger = logging.getLogger(__name__)


class RESettingService:
    @staticmethod
    def read_all(table_name):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        sql = f"""
SELECT id, label_vi, label_en, value, updated_at
FROM {table_name}
"""
        query.prepare(sql)
        if not exec_query(db, query):
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results


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
        query.prepare(sql)
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
        query.prepare(sql)
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
            query.prepare(sql)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)

            if not exec_query(db, query):
                return False
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False

    @staticmethod
    def update(table_name, payload):
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
            query.prepare(sql)
            query.bindValue(":id", id)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not exec_query(db, query):
                return False
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
            query.prepare(sql)
            query.bindValue(":id", id)
            if not exec_query(db, query):
                return False
            if not commit_db(db):
                return False
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"ERROR: {e}", exc_info=True)
            return False
