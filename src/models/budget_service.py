# src/models/budget_service.py

from strategies.budget_validation import BudgetValidationStrategy
from budget_data_collector import BudgetDataCollector
from models.budget_repository import BudgetRepository

class BudgetService:
    def __init__(self, cursor, conn, validation_strategy: BudgetValidationStrategy):
        self.cursor = cursor
        self.conn = conn
        self.data_collector = BudgetDataCollector(cursor)
        self.validator = validation_strategy
        self.repository = BudgetRepository(cursor, conn)

    def collect_budget_data(self):
        return self.data_collector.collect_budget_data()

    def insert_budget_into_db(self, presupuesto):
        if self.validator.validate(presupuesto):
            self.repository.insert_budget_into_db(presupuesto)
        else:
            raise ValueError("Presupuesto no válido")

    def add_salesperson(self):
        self.repository.add_salesperson()

    def listar_vendedores(self):
        self.repository.listar_vendedores()