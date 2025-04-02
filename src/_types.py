# src/_types.py
from typing import TypedDict, NotRequired


class RealEstateProductType(TypedDict):
    id: NotRequired[int]
    pid: str
    province_name: str
    district_name: str
    ward_name: str
    street_name: str
    category: str
    option: str
    area: float
    structure: float
    function: str
    furniture: str
    building_line: str
    legal: str
    description: str
    price: float
    updated_at: str
    created_at: NotRequired[str]
