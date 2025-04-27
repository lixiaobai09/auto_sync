import logging
import os
from logging.handlers import RotatingFileHandler
import sys


class Logger:
    def __init__(self, name, log_file_path=None):
        """Initialize logger with name and file path.

        Args:
            name (str): Logger name
            log_file_path (str, optional): Path to log file. If None, logs will only be sent to stdout.
                If specified, logs will only be sent to the file (not to stdout).
                Defaults to None.
        """
        # Configure logger
        self.logger = logging.getLogger(name)
        # set log level from environment variable or default to INFO
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level, logging.INFO)
        # print("Log level set to:", log_level)
        self.logger.setLevel(log_level)

        # Clear any existing handlers (in case of logger reuse)
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if log_file_path:
            # Create logs directory if not exists
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            # Add file handler with rotation
            file_handler = RotatingFileHandler(
                log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            # Add console handler (stdout) only if log_file_path is not provided
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """Get the configured logger.

        Returns:
            logging.Logger: Configured logger instance
        """
        return self.logger
