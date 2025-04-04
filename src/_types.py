# src/_types.py
from typing import TypedDict, NotRequired


class RealEstateProductType(TypedDict):
    id: NotRequired[int]
    image_path: NotRequired[list[str]]
    pid: str
    province: str
    district: str
    ward: str
    street: str
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
    status: int
    updated_at: str
    created_at: NotRequired[str]
