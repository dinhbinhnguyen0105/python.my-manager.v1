# src/services/real_estate_services.py
import datetime, os, shutil
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from src._types import RealEstateProductType
from src.constants import REAL_ESTATE_PRODUCT_TABLE
from src.configs.real_estate_product import RealEstateProductConfigs


class RealEstateProductService:
    @staticmethod
    def create(data: RealEstateProductType) -> bool:
        config = RealEstateProductConfigs()
        destination = os.path.join(config.image_dir(), str(data["id"]))
        RealEstateProductService.copy_files(
            data.get("image_path", []), destination, str(data["id"])
        )
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
            """
        )
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        data["updated_at"] = formatted_time
        for key, value in data.items():
            if key == "id":
                continue
            query.bindValue(f":{key}", value)
        if not query.exec():
            raise Exception(
                f"Error inserting real estate product: {query.lastError().text()}"
            )
        return True

    @staticmethod
    def read(id: int) -> RealEstateProductType:
        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT * FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE id = :id
            """
        )
        query.bindValue(":id", id)
        if not query.exec():
            raise Exception(
                f"Error fetching real estate product with id [{id}]: {query.lastError().text()}"
            )
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
            """
        )
        if not query.exec():
            raise Exception(
                f"Error fetching all real estate products: {query.lastError().text()}"
            )
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
    def update(id: int, data: dict) -> bool:
        config = RealEstateProductConfigs()
        destination = os.path.join(config.image_dir(), str(id))
        RealEstateProductService.copy_files(
            data.get("image_path", []), destination, str(id)
        )

        sql_expression_update = f"UPDATE {REAL_ESTATE_PRODUCT_TABLE} SET "
        sql_update_sets = []
        columns = RealEstateProductService.get_columns()
        for key in data.keys():
            if key in columns:
                sql_update_sets.append(f"{key} = :{key}")
        sql_expression_update += ", ".join(sql_update_sets)
        sql_expression_update += " WHERE id = :id"
        print(sql_expression_update)
        query = QSqlQuery()
        query.prepare(sql_expression_update)
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        data["updated_at"] = formatted_time
        for key, value in data.items():
            if key == "id":
                continue
            query.bindValue(f":{key}", value)
        query.bindValue(":id", id)
        if not query.exec():
            raise Exception(
                f"Error updating real estate product with id [{id}]: {query.lastError().text()}"
            )
        return True

    @staticmethod
    def delete(id: int) -> bool:
        query = QSqlQuery()
        query.prepare(
            f"""
            DELETE FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE id = :id
            """
        )
        query.bindValue(":id", id)
        if not query.exec():
            raise Exception(
                f"Error deleting real estate product with id [{id}]: {query.lastError().text()}"
            )
        return True

    @staticmethod
    def get_columns() -> list[str]:
        database = QSqlDatabase.database()
        if not database.isValid() or not database.isOpen():
            raise Exception("Database is not open or valid.")
        table_record = database.record(REAL_ESTATE_PRODUCT_TABLE)
        if table_record.isEmpty():
            raise Exception(f"Table {REAL_ESTATE_PRODUCT_TABLE} does not exist.")
        columns = []
        for i in range(table_record.count()):
            field_name = table_record.fieldName(i)
            columns.append(field_name)
        return columns

    @staticmethod
    def check_unique_pid(pid: int) -> bool:
        query = QSqlQuery()
        query.prepare(
            f"""
            SELECT pid FROM {REAL_ESTATE_PRODUCT_TABLE} WHERE pid = :pid
            """
        )
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error checking unique pid [{pid}]: {query.lastError().text()}"
            )
        if query.next():
            return True
        return False

    @staticmethod
    def copy_files(sources: list[str], destination: str, id: int) -> bool:
        os.makedirs(destination, exist_ok=True)
        destination_img_num = len(RealEstateProductService.get_images_in_directory(id))

        for index, file in enumerate(sources):
            _, extension = os.path.splitext(file)
            file_name = f"{id}_{index + destination_img_num}{extension}"
            destination_path = os.path.join(destination, file_name)
            try:
                shutil.copy2(file, destination_path)
            except FileNotFoundError:
                print(f"Error: File not found: {file}")
            except Exception as e:
                print(f"Error copying {file}: {e}")
        return True

    @staticmethod
    def delete_directory(id: int) -> bool:
        config = RealEstateProductConfigs()
        directory = os.path.abspath(os.path.join(config.image_dir(), id))
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                print(f"Error deleting directory {directory}: {e}")
                return False
        return True

    @staticmethod
    def get_images_in_directory(id: int) -> list[str]:
        config = RealEstateProductConfigs()
        directory = os.path.abspath(os.path.join(config.image_dir(), str(id)))
        if not os.path.exists(directory):
            return []
        images = []
        for file in os.listdir(directory):
            if file.endswith((".png", ".jpg", ".jpeg")):
                images.append(os.path.join(directory, file))
        return images


class RealEstateTemplateService:
    pass
