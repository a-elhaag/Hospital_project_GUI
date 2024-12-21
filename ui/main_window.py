# ui/main_window.py
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from management.hospital_management import HospitalManagement
from models.doctor import Specialization

# Light mode stylesheet
light_mode_stylesheet = """
QWidget {
    background-color: #f9f9f9;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
}

QPushButton {
    background-color: #ffffff;
    border: 2px solid #cccccc;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton:hover {
    background-color: #e6e6e6;
}

QLineEdit, QComboBox, QDateEdit, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 3px;
    padding: 4px;
}

QTableWidget {
    background-color: #ffffff;
    gridline-color: #dddddd;
}

QHeaderView::section {
    background-color: #f2f2f2;
    padding: 8px;
    border: 1px solid #cccccc;
    font-weight: bold;
}

QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #cccccc;
}

QTabBar::tab {
    background: #ffffff;
    border: 1px solid #cccccc;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: #e6e6e6;
}
"""


class MainWindow(QMainWindow):
    def __init__(self, hospital_mgmt: HospitalManagement):
        super().__init__()
        self.hospital_mgmt = hospital_mgmt
        self.setWindowTitle("Hospital Management System")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(light_mode_stylesheet)  # Apply light mode

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_patient_tab()
        self.create_doctor_tab()
        self.create_appointment_tab()

    def create_patient_tab(self):
        self.patient_tab = QWidget()
        layout = QVBoxLayout()

        # Add Patient Section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Name:"))
        self.patient_name_input = QLineEdit()
        add_layout.addWidget(self.patient_name_input)

        add_layout.addWidget(QLabel("Age:"))
        self.patient_age_input = QLineEdit()
        add_layout.addWidget(self.patient_age_input)

        add_layout.addWidget(QLabel("Medical History:"))
        self.patient_history_input = QLineEdit()
        add_layout.addWidget(self.patient_history_input)

        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(self.add_patient)
        add_layout.addWidget(add_button)

        layout.addLayout(add_layout)

        # Search Patient Section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Patient ID:"))
        self.search_patient_input = QLineEdit()
        search_layout.addWidget(self.search_patient_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_patient)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Patient Table
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(4)
        self.patient_table.setHorizontalHeaderLabels(
            ["Patient ID", "Name", "Age", "Medical History"]
        )
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patient_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.patient_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.patient_table)

        # Refresh Button
        refresh_button = QPushButton("Refresh Patient List")
        refresh_button.clicked.connect(self.load_patients)
        layout.addWidget(refresh_button)

        self.patient_tab.setLayout(layout)
        self.tabs.addTab(self.patient_tab, "Patient Management")

        # Initial Load
        self.load_patients()

    def create_doctor_tab(self):
        self.doctor_tab = QWidget()
        layout = QVBoxLayout()

        # Add Doctor Section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Name:"))
        self.doctor_name_input = QLineEdit()
        add_layout.addWidget(self.doctor_name_input)

        add_layout.addWidget(QLabel("Age:"))
        self.doctor_age_input = QLineEdit()
        add_layout.addWidget(self.doctor_age_input)

        add_layout.addWidget(QLabel("Specialization:"))
        self.doctor_specialization_input = QComboBox()
        self.doctor_specialization_input.addItems(
            [spec.value for spec in Specialization]
        )
        add_layout.addWidget(self.doctor_specialization_input)

        add_layout.addWidget(QLabel("Password:"))
        self.doctor_password_input = QLineEdit()
        self.doctor_password_input.setEchoMode(QLineEdit.Password)
        add_layout.addWidget(self.doctor_password_input)

        add_button = QPushButton("Add Doctor")
        add_button.clicked.connect(self.add_doctor)
        add_layout.addWidget(add_button)

        layout.addLayout(add_layout)

        # Search Doctor Section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Doctor ID:"))
        self.search_doctor_input = QLineEdit()
        search_layout.addWidget(self.search_doctor_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_doctor)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Doctor Table
        self.doctor_table = QTableWidget()
        self.doctor_table.setColumnCount(4)
        self.doctor_table.setHorizontalHeaderLabels(
            ["Doctor ID", "Name", "Age", "Specialization"]
        )
        self.doctor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.doctor_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.doctor_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.doctor_table)

        # Refresh Button
        refresh_button = QPushButton("Refresh Doctor List")
        refresh_button.clicked.connect(self.load_doctors)
        layout.addWidget(refresh_button)

        self.doctor_tab.setLayout(layout)
        self.tabs.addTab(self.doctor_tab, "Doctor Management")

        # Initial Load
        self.load_doctors()

    def create_appointment_tab(self):
        self.appointment_tab = QWidget()
        layout = QVBoxLayout()

        # Book Appointment Section
        book_layout = QHBoxLayout()

        # Doctor Selection
        book_layout.addWidget(QLabel("Doctor:"))
        self.appointment_doctor_combo = QComboBox()
        self.refresh_doctor_combo()
        book_layout.addWidget(self.appointment_doctor_combo)

        # Patient Selection
        book_layout.addWidget(QLabel("Patient:"))
        self.appointment_patient_combo = QComboBox()
        self.refresh_patient_combo()
        book_layout.addWidget(self.appointment_patient_combo)

        # Date Selection
        book_layout.addWidget(QLabel("Date:"))
        self.appointment_date_input = QDateEdit()
        self.appointment_date_input.setCalendarPopup(True)
        self.appointment_date_input.setDate(QDate.currentDate())
        book_layout.addWidget(self.appointment_date_input)

        # Book Button
        book_button = QPushButton("Book Appointment")
        book_button.clicked.connect(self.book_appointment)
        book_layout.addWidget(book_button)

        layout.addLayout(book_layout)

        # Appointment Table
        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(4)
        self.appointment_table.setHorizontalHeaderLabels(
            ["Appointment ID", "Doctor", "Patient", "Date"]
        )
        self.appointment_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.appointment_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.appointment_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.appointment_table.cellClicked.connect(self.display_appointment_details)
        layout.addWidget(self.appointment_table)

        # Appointment Detail Section
        detail_layout = QVBoxLayout()
        self.detail_label = QLabel("Select an appointment to see details.")
        self.detail_label.setWordWrap(True)
        detail_layout.addWidget(self.detail_label)

        # Action Buttons
        action_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit Appointment")
        self.edit_button.clicked.connect(self.edit_appointment)
        self.edit_button.setEnabled(False)
        action_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Appointment")
        self.delete_button.clicked.connect(self.delete_appointment)
        self.delete_button.setEnabled(False)
        action_layout.addWidget(self.delete_button)

        detail_layout.addLayout(action_layout)
        layout.addLayout(detail_layout)

        # Refresh Button
        refresh_button = QPushButton("Refresh Appointment List")
        refresh_button.clicked.connect(self.load_appointments)
        layout.addWidget(refresh_button)

        self.appointment_tab.setLayout(layout)
        self.tabs.addTab(self.appointment_tab, "Appointment Management")

        # Initial Load
        self.load_appointments()

    # Helper Methods to Refresh ComboBoxes
    def refresh_doctor_combo(self):
        self.appointment_doctor_combo.clear()
        self.appointment_doctor_combo.addItem("Select Doctor", "")
        for doctor in self.hospital_mgmt.list_doctors():
            display_text = f"{doctor.name} ({doctor.id})"
            self.appointment_doctor_combo.addItem(display_text, doctor.id)

    def refresh_patient_combo(self):
        self.appointment_patient_combo.clear()
        self.appointment_patient_combo.addItem("Select Patient", "")
        for patient in self.hospital_mgmt.list_patients():
            display_text = f"{patient.name} ({patient.patient_id})"
            self.appointment_patient_combo.addItem(display_text, patient.patient_id)

    # Patient Management Methods
    def add_patient(self):
        name = self.patient_name_input.text().strip()
        age_text = self.patient_age_input.text().strip()
        medical_history = self.patient_history_input.text().strip()

        if not name or not age_text or not medical_history:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a positive integer.")
            return

        new_patient = self.hospital_mgmt.add_patient(name, age, medical_history)
        QMessageBox.information(
            self, "Success", f"Patient added with ID: {new_patient.patient_id}"
        )
        self.load_patients()
        self.refresh_patient_combo()
        self.patient_name_input.clear()
        self.patient_age_input.clear()
        self.patient_history_input.clear()

    def load_patients(self):
        patients = self.hospital_mgmt.list_patients()
        self.patient_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.patient_table.setItem(row, 0, QTableWidgetItem(patient.patient_id))
            self.patient_table.setItem(row, 1, QTableWidgetItem(patient.name))
            self.patient_table.setItem(row, 2, QTableWidgetItem(str(patient.age)))
            self.patient_table.setItem(
                row, 3, QTableWidgetItem(patient.medical_history)
            )

    def search_patient(self):
        patient_id = self.search_patient_input.text().strip()
        if not patient_id:
            QMessageBox.warning(
                self, "Input Error", "Please enter a Patient ID to search."
            )
            return

        patient = self.hospital_mgmt.find_patient_by_id(patient_id)
        if patient:
            QMessageBox.information(
                self,
                "Patient Found",
                f"ID: {patient.patient_id}\nName: {patient.name}\nAge: {patient.age}\nMedical History: {patient.medical_history}",
            )
        else:
            QMessageBox.information(
                self, "Not Found", f"No patient found with ID: {patient_id}"
            )

    # Doctor Management Methods
    def add_doctor(self):
        name = self.doctor_name_input.text().strip()
        age_text = self.doctor_age_input.text().strip()
        specialization_text = self.doctor_specialization_input.currentText()
        password = self.doctor_password_input.text().strip()

        if not name or not age_text or not specialization_text or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a positive integer.")
            return

        # Get Specialization Enum
        specialization = None
        for spec in Specialization:
            if spec.value == specialization_text:
                specialization = spec
                break

        if not specialization:
            QMessageBox.warning(self, "Input Error", "Invalid specialization selected.")
            return

        new_doctor = self.hospital_mgmt.add_doctor(name, age, specialization, password)
        QMessageBox.information(
            self, "Success", f"Doctor added with ID: {new_doctor.id}"
        )
        self.load_doctors()
        self.refresh_doctor_combo()
        self.doctor_name_input.clear()
        self.doctor_age_input.clear()
        self.doctor_password_input.clear()

    def load_doctors(self):
        doctors = self.hospital_mgmt.list_doctors()
        self.doctor_table.setRowCount(len(doctors))
        for row, doctor in enumerate(doctors):
            self.doctor_table.setItem(row, 0, QTableWidgetItem(doctor.id))
            self.doctor_table.setItem(row, 1, QTableWidgetItem(doctor.name))
            self.doctor_table.setItem(row, 2, QTableWidgetItem(str(doctor.age)))
            self.doctor_table.setItem(
                row, 3, QTableWidgetItem(doctor.specialization.value)
            )

    def search_doctor(self):
        doctor_id = self.search_doctor_input.text().strip()
        if not doctor_id:
            QMessageBox.warning(
                self, "Input Error", "Please enter a Doctor ID to search."
            )
            return

        doctor = self.hospital_mgmt.find_doctor_by_id(doctor_id)
        if doctor:
            QMessageBox.information(
                self,
                "Doctor Found",
                f"ID: {doctor.id}\nName: {doctor.name}\nAge: {doctor.age}\nSpecialization: {doctor.specialization.value}",
            )
        else:
            QMessageBox.information(
                self, "Not Found", f"No doctor found with ID: {doctor_id}"
            )

    # Appointment Management Methods
    def book_appointment(self):
        doctor_id = self.appointment_doctor_combo.currentData()
        patient_id = self.appointment_patient_combo.currentData()
        date = self.appointment_date_input.date().toString("yyyy-MM-dd")

        if not doctor_id or not patient_id or not date:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        appointment = self.hospital_mgmt.book_appointment(doctor_id, patient_id, date)
        if appointment:
            QMessageBox.information(
                self,
                "Success",
                f"Appointment booked with ID: {appointment.appointment_id}",
            )
            self.load_appointments()
            self.appointment_doctor_combo.setCurrentIndex(0)
            self.appointment_patient_combo.setCurrentIndex(0)
            self.appointment_date_input.setDate(QDate.currentDate())
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to book appointment. Check Doctor and Patient selections.",
            )

    def load_appointments(self):
        appointments = self.hospital_mgmt.list_appointments()
        self.appointment_table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            self.appointment_table.setItem(
                row, 0, QTableWidgetItem(appointment.appointment_id)
            )
            doctor = self.hospital_mgmt.find_doctor_by_id(appointment.doctor_id)
            patient = self.hospital_mgmt.find_patient_by_id(appointment.patient_id)
            doctor_display = f"{doctor.name} ({doctor.id})" if doctor else "Unknown"
            patient_display = (
                f"{patient.name} ({patient.patient_id})" if patient else "Unknown"
            )
            self.appointment_table.setItem(row, 1, QTableWidgetItem(doctor_display))
            self.appointment_table.setItem(row, 2, QTableWidgetItem(patient_display))
            self.appointment_table.setItem(row, 3, QTableWidgetItem(appointment.date))

        # Clear details and disable buttons
        self.detail_label.setText("Select an appointment to see details.")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def display_appointment_details(self, row, column):
        appointment_id = self.appointment_table.item(row, 0).text()
        doctor_display = self.appointment_table.item(row, 1).text()
        patient_display = self.appointment_table.item(row, 2).text()
        date = self.appointment_table.item(row, 3).text()

        details = (
            f"Appointment ID: {appointment_id}\n"
            f"Doctor: {doctor_display}\n"
            f"Patient: {patient_display}\n"
            f"Date: {date}"
        )
        self.detail_label.setText(details)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def edit_appointment(self):
        selected_row = self.appointment_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No appointment selected.")
            return

        appointment_id = self.appointment_table.item(selected_row, 0).text()
        appointment = next(
            (
                a
                for a in self.hospital_mgmt.appointments
                if a.appointment_id == appointment_id
            ),
            None,
        )

        if not appointment:
            QMessageBox.warning(self, "Error", "Appointment not found.")
            return

        # Open Edit Dialog
        dialog = EditAppointmentDialog(appointment, self.hospital_mgmt)
        if dialog.exec():
            self.load_appointments()

    def delete_appointment(self):
        selected_row = self.appointment_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No appointment selected.")
            return

        appointment_id = self.appointment_table.item(selected_row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete appointment {appointment_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            success = self.hospital_mgmt.delete_appointment(appointment_id)
            if success:
                QMessageBox.information(
                    self, "Success", "Appointment deleted successfully."
                )
                self.load_appointments()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete appointment.")


class EditAppointmentDialog(QDialog):
    def __init__(self, appointment, hospital_mgmt: HospitalManagement):
        super().__init__()
        self.appointment = appointment
        self.hospital_mgmt = hospital_mgmt
        self.setWindowTitle(f"Edit Appointment {appointment.appointment_id}")
        self.setGeometry(150, 150, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Doctor Selection
        layout.addWidget(QLabel("Doctor:"))
        self.doctor_combo = QComboBox()
        for doctor in self.hospital_mgmt.list_doctors():
            display_text = f"{doctor.name} ({doctor.id})"
            self.doctor_combo.addItem(display_text, doctor.id)
            if doctor.id == self.appointment.doctor_id:
                self.doctor_combo.setCurrentText(display_text)
        layout.addWidget(self.doctor_combo)

        # Patient Selection
        layout.addWidget(QLabel("Patient:"))
        self.patient_combo = QComboBox()
        for patient in self.hospital_mgmt.list_patients():
            display_text = f"{patient.name} ({patient.patient_id})"
            self.patient_combo.addItem(display_text, patient.patient_id)
            if patient.patient_id == self.appointment.patient_id:
                self.patient_combo.setCurrentText(display_text)
        layout.addWidget(self.patient_combo)

        # Date Selection
        layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.fromString(self.appointment.date, "yyyy-MM-dd"))
        layout.addWidget(self.date_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_changes(self):
        new_doctor_id = self.doctor_combo.currentData()
        new_patient_id = self.patient_combo.currentData()
        new_date = self.date_input.date().toString("yyyy-MM-dd")

        if not new_doctor_id or not new_patient_id or not new_date:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        # Update appointment
        self.appointment.doctor_id = new_doctor_id
        self.appointment.patient_id = new_patient_id
        self.appointment.date = new_date

        self.hospital_mgmt.save_data()
        QMessageBox.information(self, "Success", "Appointment updated successfully.")
        self.accept()
