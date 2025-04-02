from PyQt6.QtSql import QSqlQuery
from src._types import RealEstateProductType


class RealEstateProductService:
    @staticmethod
    def create(data: RealEstateProductType) -> bool: pass
    @staticmethod
    def read(pid: str) -> RealEstateProductType: pass
    @staticmethod
    def read_all() -> list[RealEstateProductType]: pass
    @staticmethod
    def update(pid: str, data: dict) -> bool: pass
    @staticmethod
    def delete(pid: str) -> bool: pass


class RealEstateTemplateService:
    pass
