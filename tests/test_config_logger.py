"""
tests/test_config_logger.py -
Tests for the LoggerConfigurator class.
"""

import unittest
import logging
from unittest import mock
from src.logs.config_logger import LoggerConfigurator

class TestLoggerConfigurator(unittest.TestCase):
    """Test cases for LoggerConfigurator."""

    @mock.patch('os.getenv')
    @mock.patch('os.path.exists')
    @mock.patch('builtins.open', new_callable=mock.mock_open,
                read_data='{"version": 1, "disable_existing_loggers": false}')
    @mock.patch('json.load')
    @mock.patch('logging.config.dictConfig')
    def test_configure_with_valid_json(self, mock_dict_config, mock_json_load, mock_open,
                                       mock_path_exists, mock_getenv):
        """Test that configure method loads logging configuration from a valid JSON file."""
        mock_getenv.return_value = None
        mock_path_exists.return_value = True
        mock_json_load.return_value = {"version": 1, "disable_existing_loggers": False}

        configurator = LoggerConfigurator()
        logger = configurator.configure()

        mock_open.assert_called_once_with('src/logs/logging.json', 'rt', encoding='utf-8')
        mock_json_load.assert_called_once()
        mock_dict_config.assert_called_once_with({"version": 1, "disable_existing_loggers": False})
        self.assertIsInstance(logger, logging.Logger)

    @mock.patch('os.getenv')
    @mock.patch('os.path.exists')
    @mock.patch('logging.basicConfig')
    def test_configure_with_missing_json(self, mock_basic_config, mock_path_exists, mock_getenv):
        """Test that configure method falls back to basicConfig if JSON file is missing."""
        mock_getenv.return_value = None
        mock_path_exists.return_value = False

        configurator = LoggerConfigurator()
        logger = configurator.configure()

        mock_basic_config.assert_called_once_with(level=logging.INFO)
        self.assertIsInstance(logger, logging.Logger)

    @mock.patch('os.getenv')
    @mock.patch('os.path.exists')
    def test_configure_with_env_var(self, mock_path_exists, mock_getenv):
        """Test that configure method uses the path from environment variable."""
        mock_getenv.return_value = 'custom_path.json'
        mock_path_exists.return_value = True

        with mock.patch('builtins.open', mock.mock_open(
            read_data='{"version": 1, "disable_existing_loggers": false}')), \
             mock.patch('json.load', return_value={"version": 1,
                                                   "disable_existing_loggers": False}), \
             mock.patch('logging.config.dictConfig') as mock_dict_config:

            configurator = LoggerConfigurator()
            logger = configurator.configure()

            mock_getenv.assert_called_once_with('LOG_CFG', None)
            mock_dict_config.assert_called_once_with({"version": 1,
                                                      "disable_existing_loggers": False})
            self.assertIsInstance(logger, logging.Logger)
