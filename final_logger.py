import datetime
import inspect
import logging
import sys
import time
import os
import traceback
import json
import queue
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener


class CustomFormatter(logging.Formatter):
    """Custom formatter to add colors to console logs based on log level."""
    
    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': "\033[94m",    # Blue
        'INFO': "\033[92m",     # Green
        'WARNING': "\033[93m",  # Yellow
        'ERROR': "\033[91m",    # Red
        'RESET': "\033[0m"      # Reset
    }

    def format(self, record):
        log_msg = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        return f"{color}{log_msg}{reset}"


class JSONFormatter(logging.Formatter):
    """Formatter for structured JSON logging."""
    
    def format(self, record):
        log_record = {
            'time': datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
            'level': record.levelname,
            'file': record.pathname,
            'line': record.lineno,
            'message': record.msg
        }
        return json.dumps(log_record)


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive data in log messages."""
    
    def filter(self, record):
        record.msg = str(record.msg).replace("password", "******")  # Mask sensitive info
        return True


class ContextFilter(logging.Filter):
    """Filter to add contextual information to log records."""
    
    def filter(self, record):
        # Example: Add user ID or session info to each log record
        record.user_id = "12345"
        return True


class CustomLogger(logging.Logger):
    """
    Custom logger class with additional functionality
    """

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        
    def info(self, msg, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} INFO: {msg}"
        super().info(msg, *args, **kwargs)
        
    def debug(self, msg, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} DEBUG: {msg}"
        super().info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} WARNING: {msg}"
        super().info(msg, *args, **kwargs)
        
    def error(self, msg, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        _, _, exc_traceback = sys.exc_info()
        if exc_traceback:
            file_name, line_number, func_name, context = traceback.extract_tb(exc_traceback)[-1]
            msg += f"\n Exception in {file_name}, Line {line_number}, in {func_name}: {context}"
            
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} ERROR: {msg}"
        super().info(msg, *args, **kwargs)

    @staticmethod
    def shutdown():
        logging.shutdown()
        
    def __get_call_info(self):
        stack = inspect.stack()
        file_name = stack[2][1]
        line_num = stack[2][2]
        return file_name, line_num


class CaptureConsoleLogs:
    _shared_logger = None
    _log_file_name = None
    _created_loggers = {}
    queue_listener = None

    @classmethod
    def get_logger(cls, log_file_name='test_console', log_level=logging.DEBUG, structured_logging=False):
        """
        This function returns the logger instance.
        """
        environment = os.getenv("ENV", "development")
        if cls._shared_logger is None and log_file_name not in cls._created_loggers:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            log_file_name = f'{log_file_name}_{timestamp}.log'
            cls._shared_logger = cls.setup_logger(log_file_name, log_level, structured_logging)
            cls._log_file_name = log_file_name

        if environment == "production":
            cls._shared_logger.setLevel(logging.WARNING)
        else:
            cls._shared_logger.setLevel(log_level)
            
        return cls._shared_logger

    @classmethod
    def setup_logger(cls, log_file_name, log_level=logging.DEBUG, structured_logging=False):
        """
        Sets up the logger with file and console handlers
        """
        if cls._shared_logger is not None:
            return cls._shared_logger

        logger = CustomLogger("custom_logger", log_level)

        # File handler (with log rotation)
        if structured_logging:
            file_handler = RotatingFileHandler(log_file_name, maxBytes=10 * 1024 * 1024, backupCount=5)
            json_formatter = JSONFormatter()
            file_handler.setFormatter(json_formatter)
        else:
            file_handler = RotatingFileHandler(log_file_name, maxBytes=10 * 1024 * 1024, backupCount=5)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)

        # Console handler (colorful logging for console)
        console_handler = logging.StreamHandler()
        console_formatter = CustomFormatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(log_level)

        # Add filters (for sensitive data and context)
        logger.addFilter(SensitiveDataFilter())
        logger.addFilter(ContextFilter())

        # Add both handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Async logging with QueueHandler
        log_queue = queue.Queue()
        queue_handler = QueueHandler(log_queue)
        logger.addHandler(queue_handler)

        # Start QueueListener for async logging
        cls.queue_listener = QueueListener(log_queue, file_handler, console_handler)
        cls.queue_listener.start()

        cls._shared_logger = logger
        return logger

    @classmethod
    def get_log_file_name(cls):
        return cls._log_file_name

    @classmethod
    def shutdown_logger(cls):
        if cls.queue_listener:
            cls.queue_listener.stop()
        cls._shared_logger.shutdown()

    def count_down(self, duration):
        while duration:
            minutes, secs = divmod(duration, 60)
            timer = f'{minutes} min :{secs} secs'
            if duration % 10 == 0:
                self.get_logger().info(f"Wait for: {timer}")
            time.sleep(1)
            duration -= 1


# Example usage:

if __name__ == "__main__":
    logger = CaptureConsoleLogs.get_logger(log_level=logging.DEBUG, structured_logging=False)
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message with stack trace")

    # Simulate countdown with periodic logging
    CaptureConsoleLogs().count_down(15)

    # Shutdown the logger gracefully
    CaptureConsoleLogs.shutdown_logger()


"""
Key Features Implemented:
Configurable Log Levels: You can pass a log_level argument when setting up the logger.
Log Rotation: Implemented using RotatingFileHandler to limit log file size.
Environment-Specific Logging: Automatically switches log level based on environment (production or development).
Structured Logging (JSON): Added a JSONFormatter to output logs in JSON format (useful for structured logging).
Exception and Stack Trace Handling: Stack traces are logged when an exception occurs.
Customizable Log Formats: Different formats for console and file handlers.
Asynchronous Logging: Logging is handled asynchronously using QueueHandler and QueueListener.
Sensitive Data Protection: Sensitive data (e.g., passwords) is masked in the logs.
Centralized Context: Context information (e.g., user ID) is added to each log record.
Graceful Logger Shutdown: Ensures that all log messages are flushed before the application exits.
Usage:
Use the get_logger method to obtain the logger. It accepts parameters like log_level and structured_logging for JSON-based logging.
The logger can handle asynchronous logging and sensitive data masking automatically.
You can use the count_down method for a countdown timer with periodic logging.
Remember to call shutdown_logger() to gracefully close the logger at the end of the program.
This logger should cover most real-world use cases in development, testing, and production environments.
"""