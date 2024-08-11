# src/models/salesperson_manager.py

from src.interfaces.salesperson_interface import SalespersonLister, SalespersonCreator

class SalespersonManager(SalespersonLister, SalespersonCreator):
    def list_salespersons(self):
        # Implementation for listing salespersons
        pass

    def create_salesperson(self, name: str, email: str):
        # Implementation for creating a salesperson
        pass