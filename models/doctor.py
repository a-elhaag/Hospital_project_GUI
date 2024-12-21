# models/doctor.py
from enum import Enum

from models.human import Human


class Specialization(Enum):
    GENERAL = "General"
    CARDIOLOGIST = "Cardiologist"
    NEUROLOGIST = "Neurologist"
    PEDIATRICIAN = "Pediatrician"
    SURGEON = "Surgeon"


class Doctor(Human):
    _doc_counter = 0  # Static member to keep track of doctor IDs

    def __init__(
        self,
        name: str,
        age: int,
        specialization: Specialization,
        password: str,
        id: str = None,
    ):
        super().__init__(name, age)
        if id:
            self.id = id
            current_id_num = int(id[1:])
            if current_id_num > Doctor._doc_counter:
                Doctor._doc_counter = current_id_num
        else:
            Doctor._doc_counter += 1
            self.id = f"D{Doctor._doc_counter}"
        self.specialization = specialization
        self.password = password  # In a real system, passwords should be hashed

    def display_info(self):
        print(
            f"Doctor ID: {self.id}, Name: {self.name}, Age: {self.age}, "
            f"Specialization: {self.specialization.value}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "specialization": self.specialization.value,
            "password": self.password,
        }

    @staticmethod
    def from_dict(data: dict):
        specialization = Specialization(data["specialization"])
        return Doctor(
            name=data["name"],
            age=data["age"],
            specialization=specialization,
            password=data["password"],
            id=data["id"],
        )
