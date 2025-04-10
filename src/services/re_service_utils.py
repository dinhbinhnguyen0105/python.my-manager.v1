# src/services/re_service_utils.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import logging

logger = logging.getLogger(__name__)


def commit_db(db):
    if not db.commit():
        logger.error("Failed to commit transaction.")
        return False
    return True


def exec_query(db, query):
    sql = query.lastQuery()
    if not query.exec():
        logger.error(
            f"Error executing SQL query: {sql}\nERROR message: {query.lastError().text()}"
        )
        db.rollback()
        return False
    return True


def is_tid_existed(table_name, tid):
    db = QSqlDatabase.database()
    query = QSqlQuery(db)
    sql = f"""
SELECT COUNT(*) FROM {table_name}
WHERE tid = :tid
"""
    query.prepare(sql)
    query.bindValue("tid", tid)
    if not exec_query(db, query):
        return False
    if query.next():
        return query.value(0) > 0
    return False


def get_columns(table_name):
    db = QSqlDatabase.database()
    record = db.record(table_name)
    if record.isEmpty():
        logger.info(f"Table {table_name} does not exist.")
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
SELECT id FROM {table_name} WHERE {condition.keys()[0]} = {condition.values()[0]}
"""
    query.prepare(sql)
    if not exec_query(db, query):
        return []
    ids = []
    while query.next():
        ids.append(query.value(0))
    return ids
