# models/patient.py
from models.human import Human


class Patient(Human):
    _patient_counter = 0  # Static member to keep track of patient IDs

    def __init__(
        self, name: str, age: int, medical_history: str, patient_id: str = None
    ):
        super().__init__(name, age)
        if patient_id:
            self.patient_id = patient_id
            current_id_num = int(patient_id[1:])
            if current_id_num > Patient._patient_counter:
                Patient._patient_counter = current_id_num
        else:
            Patient._patient_counter += 1
            self.patient_id = f"P{Patient._patient_counter}"
        self.medical_history = medical_history

    def display_info(self):
        print(
            f"Patient ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, "
            f"Medical History: {self.medical_history}"
        )

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "medical_history": self.medical_history,
        }

    @staticmethod
    def from_dict(data: dict):
        return Patient(
            name=data["name"],
            age=data["age"],
            medical_history=data["medical_history"],
            patient_id=data["patient_id"],
        )
