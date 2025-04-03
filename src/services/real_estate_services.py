import datetime
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from src._types import RealEstateProductType
from src.constants import REAL_ESTATE_PRODUCT_TABLE


class RealEstateProductService:
    @staticmethod
    def create(data: RealEstateProductType) -> bool:
        query = QSqlQuery()
        query.prepare(
            f"""
            INSERT INTO {REAL_ESTATE_PRODUCT_TABLE} (
                pid, province, district, ward, street,
                option, category,
                area, structure, function, furniture,
                building_line, legal, description, status,
                price, updated_at
            ) VALUES (:pid, :province, :district, :ward, :street,
                :option, :category,
                :area, :structure, :function, :furniture,
                :building_line, :legal, :description, :status,
                :price, :updated_at
            )
            """)
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        data["updated_at"] = formatted_time
        for key, value in data.items():
            if key == "id":
                continue
            query.bindValue(f":{key}", value)
        if not query.exec():
            raise Exception(
                f"Error inserting real estate product: {query.lastError().text()}")
        return True

    @staticmethod
    def read(pid: str) -> RealEstateProductType:
        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT * FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE pid = :pid
            """)
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error fetching real estate product with pid [{pid}]: {query.lastError().text()}")
        if query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = record.value(i)
                data[field_name] = field_value
            return data
        return {}

    @staticmethod
    def read_all() -> list[RealEstateProductType]:
        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT * FROM {REAL_ESTATE_PRODUCT_TABLE}
            """)
        if not query.exec():
            raise Exception(
                f"Error fetching all real estate products: {query.lastError().text()}")
        products = []
        while query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = record.value(i)
                data[field_name] = field_value
            products.append(data)
        return products

    @staticmethod
    def update(pid: str, data: dict) -> bool:
        sql_expression_update = "UPDATE {REAL_ESTATE_PRODUCT_TABLE} SET "
        sql_update_sets = []
        columns = RealEstateProductService.get_columns()
        for key in data.keys():
            if key not in columns:
                raise Exception(
                    f"Invalid column name [{key}] for table {REAL_ESTATE_PRODUCT_TABLE}.")
            else:
                sql_update_sets.append(f"{key} = :{key}")
        sql_expression_update += ", ".join(sql_update_sets)
        sql_expression_update += " WHERE pid = :pid"
        query = QSqlQuery()
        query.prepare(sql_expression_update)
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        data["updated_at"] = formatted_time
        for key, value in data.items():
            if key == "id":
                continue
            query.bindValue(f":{key}", value)
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error updating real estate product with pid [{pid}]: {query.lastError().text()}")
        return True

    @staticmethod
    def delete(pid: str) -> bool:
        query = QSqlQuery()
        query.prepare(
            f"""
            DELETE FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE pid = :pid
            """)
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error deleting real estate product with pid [{pid}]: {query.lastError().text()}")
        return True

    @staticmethod
    def get_columns() -> list[str]:
        database = QSqlDatabase.database()
        if not database.isValid() or not database.isOpen():
            raise Exception("Database is not open or valid.")
        table_record = database.record(REAL_ESTATE_PRODUCT_TABLE)
        if table_record.isEmpty():
            raise Exception(
                f"Table {REAL_ESTATE_PRODUCT_TABLE} does not exist.")
        columns = []
        for i in range(table_record.count()):
            field_name = table_record.fieldName(i)
            columns.append(field_name)
        return columns

    @staticmethod
    def check_unique_pid(pid: str) -> bool:
        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT pid FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE pid = :pid
            """)
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error checking unique pid [{pid}]: {query.lastError().text()}")
        if query.next():
            return True
        return False


class RealEstateTemplateService:
    pass
