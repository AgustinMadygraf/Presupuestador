# src/models/budget_service.py

"""
This module provides the BudgetService class which handles budget-related operations
such as collecting budget data, inserting budgets into the database, and managing salespersons.
"""

from src.strategies.budget_validation import BudgetValidationStrategy
from src.budget_data_collector import BudgetDataCollector
from src.models.budget_repository import BudgetRepository

class BudgetService:
    """
    BudgetService handles the business logic for budget operations.
    """

    def __init__(self, cursor, conn, validation_strategy: BudgetValidationStrategy):
        """
        Initialize the BudgetService with a database cursor, connection, and validation strategy.

        :param cursor: Database cursor for executing queries.
        :param conn: Database connection object.
        :param validation_strategy: Strategy for validating budget data.
        """
        self.cursor = cursor
        self.conn = conn
        self.data_collector = BudgetDataCollector(cursor)
        self.validator = validation_strategy
        self.repository = BudgetRepository(cursor, conn)

    def collect_budget_data(self):
        """
        Collect budget data using the data collector.

        :return: Collected budget data.
        """
        return self.data_collector.collect_budget_data()

    def insert_budget_into_db(self, presupuesto):
        """
        Insert a validated budget into the database.

        :param presupuesto: Budget data to be inserted.
        :raises ValueError: If the budget data is not valid.
        """
        if self.validator.validate(presupuesto):
            self.repository.insert_budget_into_db(presupuesto)
        else:
            raise ValueError("Presupuesto no válido")

    def add_salesperson(self):
        """
        Add a salesperson to the database.
        """
        self.repository.add_salesperson()

    def listar_vendedores(self):
        """
        List all salespersons from the database.
        """
        self.repository.listar_vendedores()
