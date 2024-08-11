# src/logs/ExcludeHTTPLogsFilter.py
import logging

class ExcludeHTTPLogsFilter(logging.Filter):
    def filter(self, record):
        # Filtrar mensajes que contienen "GET / HTTP/1.1" y similares
        return 'GET /' not in record.getMessage() and 'POST /' not in record.getMessage()
