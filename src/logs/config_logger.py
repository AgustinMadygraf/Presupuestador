# src/logs/config_logger.py

import logging.config
import os
import json

class LoggerConfigurator:
    def __init__(self, default_path='src/logs/logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
        self.default_path = default_path
        self.default_level = default_level
        self.env_key = env_key
        self.logger = self.configure_logging()

    def configure_logging(self):
        path = self.default_path
        value = os.getenv(self.env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=self.default_level)
        return logging.getLogger(__name__)

    def get_logger(self):
        return self.logger

class InfoErrorFilter(logging.Filter):
    def filter(self, record):
        # Permitir solo registros de nivel INFO y ERROR
        return record.levelno in (logging.INFO, logging.ERROR)

# Configuración inicial del logger para módulos individuales
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()
