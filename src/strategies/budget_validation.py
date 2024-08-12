# src/strategies/budget_validation.py
from src.models.presupuesto import Presupuesto
from abc import ABC, abstractmethod

class BudgetValidationStrategy(ABC):
    @abstractmethod
    def validate(self, presupuesto: Presupuesto) -> bool:
        pass

class BasicBudgetValidationStrategy(BudgetValidationStrategy):
    def validate(self, presupuesto: Presupuesto) -> bool:
        # Implement basic validation logic
        return True

class AdvancedBudgetValidationStrategy(BudgetValidationStrategy):
    def validate(self, presupuesto: Presupuesto) -> bool:
        # Implement advanced validation logic
        return True