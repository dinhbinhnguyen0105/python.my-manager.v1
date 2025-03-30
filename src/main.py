# src/main.py
import sys
from src.app import App


def main():
    """Entry point chính của ứng dụng"""
    app = App(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
