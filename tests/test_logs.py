"""
tests/test_logs.py
Tests for LoggerConfigurator, ExcludeHTTPLogsFilter, and InfoErrorFilter.
"""

import unittest
import logging
from unittest import mock
from src.logs.config_logger import LoggerConfigurator
from src.logs.exclude_http_logs_filter import ExcludeHTTPLogsFilter
from src.logs.info_error_filter import InfoErrorFilter

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

class TestExcludeHTTPLogsFilter(unittest.TestCase):
    """Test cases for ExcludeHTTPLogsFilter."""

    def setUp(self):
        """Set up a log record and the filter before each test."""
        self.filter = ExcludeHTTPLogsFilter()
        self.logger = logging.getLogger('test_logger')

    def test_filter_allows_non_http_logs(self):
        """Test that non-HTTP log records pass through the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.INFO,
                                       pathname='', lineno=0,
                                       msg='Some regular log message', args=(), exc_info=None)
        self.assertTrue(self.filter.filter(log_record))

    def test_filter_excludes_get_requests(self):
        """Test that HTTP GET log records are excluded by the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.INFO,
                                       pathname='', lineno=0,
                                       msg='GET /some-endpoint', args=(), exc_info=None)
        self.assertFalse(self.filter.filter(log_record))

    def test_filter_excludes_post_requests(self):
        """Test that HTTP POST log records are excluded by the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.INFO,
                                       pathname='', lineno=0,
                                       msg='POST /some-endpoint', args=(), exc_info=None)
        self.assertFalse(self.filter.filter(log_record))

    def test_filter_allows_other_messages(self):
        """Test that log records with different messages pass through the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.INFO,
                                       pathname='', lineno=0,
                                       msg='This is a log message', args=(), exc_info=None)
        self.assertTrue(self.filter.filter(log_record))

class TestInfoErrorFilter(unittest.TestCase):
    """Test cases for InfoErrorFilter."""

    def setUp(self):
        """Set up a log record and the filter before each test."""
        self.filter = InfoErrorFilter()
        self.logger = logging.getLogger('test_logger')

    def test_filter_allows_info_logs(self):
        """Test that INFO level log records pass through the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.INFO,
                                       pathname='', lineno=0,
                                       msg='This is an INFO log message', args=(), exc_info=None)
        self.assertTrue(self.filter.filter(log_record))

    def test_filter_allows_error_logs(self):
        """Test that ERROR level log records pass through the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.ERROR,
                                       pathname='', lineno=0,
                                       msg='This is an ERROR log message', args=(), exc_info=None)
        self.assertTrue(self.filter.filter(log_record))

    def test_filter_excludes_debug_logs(self):
        """Test that DEBUG level log records are excluded by the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.DEBUG,
                                       pathname='', lineno=0,
                                       msg='This is a DEBUG log message', args=(), exc_info=None)
        self.assertFalse(self.filter.filter(log_record))

    def test_filter_excludes_warning_logs(self):
        """Test that WARNING level log records are excluded by the filter."""
        log_record = logging.LogRecord(name='test_logger', level=logging.WARNING,
                                       pathname='', lineno=0,
                                       msg='This is a WARNING log message', args=(), exc_info=None)
        self.assertFalse(self.filter.filter(log_record))

if __name__ == '__main__':
    unittest.main()
