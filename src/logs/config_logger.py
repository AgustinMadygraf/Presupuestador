# src/logs/config_logger.py
import logging.config
import os
import json

class LoggerConfigurator:
    def __init__(self, config_path='src/logs/logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
        self.config_path = config_path
        self.default_level = default_level
        self.env_key = env_key

    def configure(self):
        path = self.config_path
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

# Configuración inicial del logger para módulos individuales
logger_configurator = LoggerConfigurator()
