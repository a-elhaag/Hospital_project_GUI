# models/human.py
from abc import ABC, abstractmethod


class Human(ABC):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if value <= 0:
            raise ValueError("Age must be positive.")
        self._age = value

    @abstractmethod
    def display_info(self):
        pass
