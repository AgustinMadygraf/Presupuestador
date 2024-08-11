# src/interfaces/salesperson_interface.py

from abc import ABC, abstractmethod

class SalespersonLister(ABC):
    @abstractmethod
    def list_salespersons(self):
        pass

class SalespersonCreator(ABC):
    @abstractmethod
    def create_salesperson(self, name: str, email: str):
        pass