"""
src/logs/InfoErrorFilter.py
Filter module for allowing only INFO and ERROR logs.
"""

import logging

class InfoErrorFilter(logging.Filter):
    """Filters logs to allow only INFO and ERROR levels."""

    def __init__(self):
        super().__init__()

    def filter(self, record):
        """Allow log records with level INFO or ERROR."""
        return record.levelno in (logging.INFO, logging.ERROR)
