# management/hospital_management.py
import json
import os
from typing import List, Optional

from models.appointment import Appointment
from models.doctor import Doctor, Specialization
from models.patient import Patient


class HospitalManagement:
    def __init__(self):
        self.doctors: List[Doctor] = []
        self.patients: List[Patient] = []
        self.appointments: List[Appointment] = []
        self.load_data()

    # Doctor Management
    def add_doctor(
        self, name: str, age: int, specialization: Specialization, password: str
    ) -> Doctor:
        new_doctor = Doctor(name, age, specialization, password)
        self.doctors.append(new_doctor)
        self.save_data()
        return new_doctor

    def list_doctors(self) -> List[Doctor]:
        return self.doctors

    def find_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                return doctor
        return None

    # Patient Management
    def add_patient(self, name: str, age: int, medical_history: str) -> Patient:
        new_patient = Patient(name, age, medical_history)
        self.patients.append(new_patient)
        self.save_data()
        return new_patient

    def list_patients(self) -> List[Patient]:
        return self.patients

    def find_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        for patient in self.patients:
            if patient.patient_id == patient_id:
                return patient
        return None

    # Appointment Management
    def book_appointment(
        self, doctor_id: str, patient_id: str, date: str
    ) -> Optional[Appointment]:
        doctor = self.find_doctor_by_id(doctor_id)
        patient = self.find_patient_by_id(patient_id)
        if doctor and patient:
            new_appointment = Appointment(doctor_id, patient_id, date)
            self.appointments.append(new_appointment)
            self.save_data()
            return new_appointment
        return None

    def list_appointments(self) -> List[Appointment]:
        return self.appointments

    def delete_appointment(self, appointment_id: str) -> bool:
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                self.appointments.remove(appointment)
                self.save_data()
                return True
        return False

    # Data Persistence
    def save_data(self):
        # Save Doctors
        with open("doctors.json", "w") as f:
            json.dump([doctor.to_dict() for doctor in self.doctors], f, indent=4)

        # Save Patients
        with open("patients.json", "w") as f:
            json.dump([patient.to_dict() for patient in self.patients], f, indent=4)

        # Save Appointments
        with open("appointments.json", "w") as f:
            json.dump(
                [appointment.to_dict() for appointment in self.appointments],
                f,
                indent=4,
            )

    def load_data(self):
        # Load Doctors
        if os.path.exists("doctors.json"):
            with open("doctors.json", "r") as f:
                doctors_data = json.load(f)
                for doc_dict in doctors_data:
                    doctor = Doctor.from_dict(doc_dict)
                    self.doctors.append(doctor)

        # Load Patients
        if os.path.exists("patients.json"):
            with open("patients.json", "r") as f:
                patients_data = json.load(f)
                for pat_dict in patients_data:
                    patient = Patient.from_dict(pat_dict)
                    self.patients.append(patient)

        # Load Appointments
        if os.path.exists("appointments.json"):
            with open("appointments.json", "r") as f:
                appointments_data = json.load(f)
                for app_dict in appointments_data:
                    appointment = Appointment.from_dict(app_dict)
                    self.appointments.append(appointment)
