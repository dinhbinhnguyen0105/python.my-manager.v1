from PyQt6.QtWidgets import QApplication
from src.controllers.user_controller import UserController
from src.models.user_database import initialize_user_db

if __name__ == "__main__":
    app = QApplication([])
    if not initialize_user_db():
        print("ERROR initialize_user_db")
        exit()

    controller = UserController()
    payload = {
        "status": 1,
        "uid": "uid_5",
        "username": "username_5",
        "password": "password_5",
        "two_fa": "two_fa_5",
        "email": "email_5",
        "email_password": "email_password_5",
        "phone_number": "phone_number_5",
        "note": "note_5",
        "type": "type_5",
        "user_group": "user_group_5",
    }
    controller.create(payload)
    controller.delete(1)
    controller.delete(2)
    controller.delete(3)
    controller.delete(4)
    controller.delete(5)
    _all = controller.read_all()
    print(_all)
