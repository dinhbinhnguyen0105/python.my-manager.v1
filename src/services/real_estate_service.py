# src/services/real_estate_service.py
from PyQt6.QtSql import QSqlQuery


class RealEstateService:
    @staticmethod
    def create_real_estate(data):
        option_name = data.get("option")
        option_id = RealEstateService._get_option_id(option_name)
        if option_id is None:
            return False

        category_name = data.get("category")
        category_id = RealEstateService._get_category_id(category_name)
        if category_id is None:
            return False

        province_name = data.get("province")
        province_id = RealEstateService._get_province_id(province_name)
        if province_id is None:
            return False

        district_name = data.get("district")
        district_id = RealEstateService._get_district_id(district_name)
        if district_id is None:
            return False

        ward_name = str(data.get("ward"))  # Đảm bảo ward là string để truy vấn
        ward_id = RealEstateService._get_ward_id(ward_name)
        if ward_id is None:
            return False

        furniture_name = data.get("furniture")
        furniture_id = RealEstateService._get_furniture_id(furniture_name)
        # furniture_id có thể là None, không cần kiểm tra ở đây

        legal_name = data.get("legal")
        legal_id = RealEstateService._get_legal_id(legal_name)
        # legal_id có thể là None, không cần kiểm tra ở đây

        building_line_name = data.get("building_line")
        building_line_id = RealEstateService._get_building_line_id(
            building_line_name)
        if building_line_id is None:
            return False

        query = QSqlQuery()
        query.prepare("""
        INSERT INTO real_estate (
            pid, option_id, category_id, province_id, district_id, ward_id,
            furniture_id, legal_id, building_line_id, street, area,
            structure, function, price, description, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(data.get("id"))
        query.addBindValue(option_id)
        query.addBindValue(category_id)
        query.addBindValue(province_id)
        query.addBindValue(district_id)
        query.addBindValue(ward_id)
        query.addBindValue(furniture_id)
        query.addBindValue(legal_id)
        query.addBindValue(building_line_id)
        query.addBindValue(data.get("street"))
        query.addBindValue(data.get("area"))
        query.addBindValue(data.get("structure"))
        query.addBindValue(data.get("function"))
        query.addBindValue(data.get("price"))
        query.addBindValue(data.get("description"))
        query.addBindValue(data.get("status", 1))

        if query.exec():
            return True
        else:
            print(
                f"[ERROR] Failed to create real estate - ERROR: {query.lastError().text()}")
            return False

    @staticmethod
    def read_real_estate(pid):
        query = QSqlQuery()
        query.prepare("""
            SELECT
                r.pid,
                ro.name AS option,
                rc.name AS category,
                rp.name AS province,
                rd.name AS district,
                rw.name AS ward,
                rfu.name AS furniture,
                rl.name AS legal,
                rbl.name AS building_line,
                r.street,
                r.area,
                r.structure,
                r.function,
                r.price,
                r.description,
                r.status,
                r.createdAt,
                r.updatedAt
            FROM real_estate r
            LEFT JOIN real_estate_options ro ON r.option_id = ro.id
            LEFT JOIN real_estate_categories rc ON r.category_id = rc.id
            LEFT JOIN real_estate_provinces rp ON r.province_id = rp.id
            LEFT JOIN real_estate_districts rd ON r.district_id = rd.id
            LEFT JOIN real_estate_wards rw ON r.ward_id = rw.id
            LEFT JOIN real_estate_furniture rfu ON r.furniture_id = rfu.id
            LEFT JOIN real_estate_legal rl ON r.legal_id = rl.id
            LEFT JOIN real_estate_building_line rbl ON r.building_line_id = rbl.id
            WHERE r.pid = ?
        """)
        query.addBindValue(pid)
        if query.exec() and query.next():
            return {
                'pid': query.value('pid'),
                'option': query.value('option'),
                'category': query.value('category'),
                'province': query.value('province'),
                'district': query.value('district'),
                'ward': query.value('ward'),
                'furniture': query.value('furniture'),
                'legal': query.value('legal'),
                'building_line': query.value('building_line'),
                'street': query.value('street'),
                'area': query.value('area'),
                'structure': query.value('structure'),
                'function': query.value('function'),
                'price': query.value('price'),
                'description': query.value('description'),
                'status': query.value('status'),
                'createdAt': query.value('createdAt'),
                'updatedAt': query.value('updatedAt')
            }
        else:
            raise Exception(
                f"[ERROR] Real estate with PID '{pid}' not found - ERROR: {query.lastError().text()}")

    @staticmethod
    def read_all_real_estates():
        query = QSqlQuery()
        query.prepare("""
            SELECT
                r.pid,
                ro.name AS option,
                rc.name AS category,
                rp.name AS province,
                rd.name AS district,
                rw.name AS ward,
                rfu.name AS furniture,
                rl.name AS legal,
                rbl.name AS building_line,
                r.street,
                r.area,
                r.structure,
                r.function,
                r.price,
                r.description,
                r.status
            FROM real_estate r
            LEFT JOIN real_estate_options ro ON r.option_id = ro.id
            LEFT JOIN real_estate_categories rc ON r.category_id = rc.id
            LEFT JOIN real_estate_provinces rp ON r.province_id = rp.id
            LEFT JOIN real_estate_districts rd ON r.district_id = rd.id
            LEFT JOIN real_estate_wards rw ON r.ward_id = rw.id
            LEFT JOIN real_estate_furniture rfu ON r.furniture_id = rfu.id
            LEFT JOIN real_estate_legal rl ON r.legal_id = rl.id
            LEFT JOIN real_estate_building_line rbl ON r.building_line_id = rbl.id
        """)
        real_estates = []
        if query.exec():
            while query.next():
                real_estates.append({
                    'pid': query.value('pid'),
                    'option': query.value('option'),
                    'category': query.value('category'),
                    'province': query.value('province'),
                    'district': query.value('district'),
                    'ward': query.value('ward'),
                    'furniture': query.value('furniture'),
                    'legal': query.value('legal'),
                    'building_line': query.value('building_line'),
                    'street': query.value('street'),
                    'area': query.value('area'),
                    'structure': query.value('structure'),
                    'function': query.value('function'),
                    'price': query.value('price'),
                    'description': query.value('description'),
                    'status': query.value('status')
                })
        else:
            raise Exception(
                f"[ERROR] Failed to read all real estates - ERROR: {query.lastError().text()}")
        return real_estates

    @staticmethod
    def update_real_estate(pid, data):
        option_name = data.get("option")
        option_id = RealEstateService._get_option_id(option_name)
        if option_id is None and "option" in data:  # Chỉ kiểm tra nếu 'option' có trong data
            return False

        category_name = data.get("category")
        category_id = RealEstateService._get_category_id(category_name)
        if category_id is None and "category" in data:
            return False

        province_name = data.get("province")
        province_id = RealEstateService._get_province_id(province_name)
        if province_id is None and "province" in data:
            return False

        district_name = data.get("district")
        district_id = RealEstateService._get_district_id(district_name)
        if district_id is None and "district" in data:
            return False

        ward_name = str(data.get("ward"))
        ward_id = RealEstateService._get_ward_id(ward_name)
        if ward_id is None and "ward" in data:
            return False

        furniture_name = data.get("furniture")
        furniture_id = RealEstateService._get_furniture_id(furniture_name)
        # furniture_id có thể là None

        legal_name = data.get("legal")
        legal_id = RealEstateService._get_legal_id(legal_name)
        # legal_id có thể là None

        building_line_name = data.get("building_line")
        building_line_id = RealEstateService._get_building_line_id(
            building_line_name)
        if building_line_id is None and "building_line" in data:
            return False

        query = QSqlQuery()
        sql = """
            UPDATE real_estate
            SET
        """
        updates = []
        if "option" in data:
            updates.append("option_id = ?")
        if "category" in data:
            updates.append("category_id = ?")
        if "province" in data:
            updates.append("province_id = ?")
        if "district" in data:
            updates.append("district_id = ?")
        if "ward" in data:
            updates.append("ward_id = ?")
        if "furniture" in data:
            updates.append("furniture_id = ?")
        if "legal" in data:
            updates.append("legal_id = ?")
        if "building_line" in data:
            updates.append("building_line_id = ?")
        if "street" in data:
            updates.append("street = ?")
        if "area" in data:
            updates.append("area = ?")
        if "structure" in data:
            updates.append("structure = ?")
        if "function" in data:
            updates.append("function = ?")
        if "price" in data:
            updates.append("price = ?")
        if "description" in data:
            updates.append("description = ?")
        if "status" in data:
            updates.append("status = ?")
        updates.append("updatedAt = strftime('%Y-%m-%d %H:%M:%S', 'now')")

        sql += ", ".join(updates)
        sql += " WHERE pid = ?"
        query.prepare(sql)

        bind_values = []
        if "option" in data:
            bind_values.append(option_id)
        if "category" in data:
            bind_values.append(category_id)
        if "province" in data:
            bind_values.append(province_id)
        if "district" in data:
            bind_values.append(district_id)
        if "ward" in data:
            bind_values.append(ward_id)
        if "furniture" in data:
            bind_values.append(furniture_id)
        if "legal" in data:
            bind_values.append(legal_id)
        if "building_line" in data:
            bind_values.append(building_line_id)
        if "street" in data:
            bind_values.append(data.get("street"))
        if "area" in data:
            bind_values.append(data.get("area"))
        if "structure" in data:
            bind_values.append(data.get("structure"))
        if "function" in data:
            bind_values.append(data.get("function"))
        if "price" in data:
            bind_values.append(data.get("price"))
        if "description" in data:
            bind_values.append(data.get("description"))
        if "status" in data:
            bind_values.append(data.get("status"))
        bind_values.append(pid)

        for value in bind_values:
            query.addBindValue(value)

        if query.exec():
            return True
        else:
            raise Exception(
                f"[ERROR] Failed to update real estate with PID '{pid}' - ERROR: {query.lastError().text()}")

    @staticmethod
    def delete_real_estate(pid):
        query = QSqlQuery()
        query.prepare("""
                DELETE FROM real_estate
                WHERE pid = ?
            """)
        query.addBindValue(pid)

        if query.exec():
            return True
        else:
            raise Exception(
                f"[ERROR] Failed to delete real estate with PID '{pid}' - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_option_id(option_name):
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_options WHERE name = ?")
        query.addBindValue(option_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] option_name not found: {option_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_category_id(category_name):
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_categories WHERE name = ?")
        query.addBindValue(category_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] category_name not found: {category_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_province_id(province_name):
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_provinces WHERE name = ?")
        query.addBindValue(province_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] province_name not found: {province_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_ward_id(ward_name):
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_wards WHERE name = ?")
        query.addBindValue(ward_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] ward_name not found: {ward_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_furniture_id(furniture_name):
        if not furniture_name:
            return None
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_furniture WHERE name = ?")
        query.addBindValue(furniture_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] furniture_name not found: {furniture_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_legal_id(legal_name):
        if not legal_name:
            return None
        query = QSqlQuery()
        query.prepare("SELECT id FROM real_estate_legal WHERE name = ?")
        query.addBindValue(legal_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] legal_name not found: {legal_name} - ERROR: {query.lastError().text()}")

    @staticmethod
    def _get_building_line_id(building_line_name):
        query = QSqlQuery()
        query.prepare(
            "SELECT id FROM real_estate_building_line WHERE name = ?")
        query.addBindValue(building_line_name)
        if query.exec() and query.next():
            return query.value(0)
        else:
            raise Exception(
                f"[ERROR] building_line_name not found: {building_line_name} - ERROR: {query.lastError().text()}")
