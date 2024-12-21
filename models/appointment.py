# models/appointment.py


class Appointment:
    _appointment_counter = 0  # Static member to keep track of appointment IDs

    def __init__(
        self, doctor_id: str, patient_id: str, date: str, appointment_id: str = None
    ):
        if appointment_id:
            self.appointment_id = appointment_id
            current_id_num = int(appointment_id[1:])
            if current_id_num > Appointment._appointment_counter:
                Appointment._appointment_counter = current_id_num
        else:
            Appointment._appointment_counter += 1
            self.appointment_id = f"A{Appointment._appointment_counter}"
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date = date

    def display_info(self):
        print(
            f"Appointment ID: {self.appointment_id}, Doctor ID: {self.doctor_id}, "
            f"Patient ID: {self.patient_id}, Date: {self.date}"
        )

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data: dict):
        return Appointment(
            doctor_id=data["doctor_id"],
            patient_id=data["patient_id"],
            date=data["date"],
            appointment_id=data["appointment_id"],
        )
