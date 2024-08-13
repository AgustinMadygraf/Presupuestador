"""
src/logs/config_logger.py
Logger configuration module.
"""

import logging.config
import os
import json
from src.logs.exclude_http_logs_filter import ExcludeHTTPLogsFilter
from src.logs.info_error_filter import InfoErrorFilter

class LoggerConfigurator:
    """Configures logging for the application."""
    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        config_path='src/logs/logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
    ):
        self.config_path = config_path
        self.default_level = default_level
        self.env_key = env_key

    def configure(self):
        """Configures the logger using a JSON file or basic configuration."""
        path = self.config_path
        value = os.getenv(self.env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt', encoding='utf-8') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=self.default_level)
        return logging.getLogger(__name__)

# Configuración inicial del logger para módulos individuales
logger_configurator = LoggerConfigurator()
logger = logger_configurator.configure()
#logger.addFilter(ExcludeHTTPLogsFilter())
logger.addFilter(InfoErrorFilter())
