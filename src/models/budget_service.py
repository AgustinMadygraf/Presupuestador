# src/models/budget_service.py
from src.models.budget_repository import BudgetRepository
from budget_data_collector import BudgetDataCollector
from budget_validator import BudgetValidator

class BudgetService:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn
        self.data_collector = BudgetDataCollector(cursor)
        self.validator = BudgetValidator()
        self.repository = BudgetRepository(cursor, conn)

    def collect_budget_data(self):
        return self.data_collector.collect_budget_data()

    def insert_budget_into_db(self, presupuesto):
        self.repository.insert_budget_into_db(presupuesto)

    def add_salesperson(self):
        self.repository.add_salesperson()

    def listar_vendedores(self):
        self.repository.listar_vendedores()