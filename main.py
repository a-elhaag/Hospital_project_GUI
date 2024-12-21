# main.py
import sys

from PySide6.QtWidgets import QApplication

from management.hospital_management import HospitalManagement
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    hospital_mgmt = HospitalManagement()
    window = MainWindow(hospital_mgmt)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
