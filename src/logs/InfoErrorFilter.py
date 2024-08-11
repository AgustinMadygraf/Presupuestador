# src/logs/InfoErrorFilter.py
import logging

class InfoErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.ERROR)
