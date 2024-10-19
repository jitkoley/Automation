import logging
import inspect
import traceback
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from colorama import Fore, Style, init
import threading

# Initialize colorama for cross-platform support
init(autoreset=True)

class CustomLogger:
    def __init__(self, name: str, log_to_file: bool = False, log_file: str = 'app.log', max_file_size: int = 5 * 1024 * 1024, backup_count: int = 5):
        """
        Custom Logger class.
        
        :param name: Name of the logger.
        :param log_to_file: Enable logging to file.
        :param log_file: Path to log file.
        :param max_file_size: Max file size for log rotation in bytes.
        :param backup_count: Number of backup files to retain.
        """
        # Create a logger with the given name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        if log_to_file:
            # Rotating file handler for log rotation by size
            file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - [PID:%(process)d] [TID:%(thread)d] - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Optionally add TimedRotatingFileHandler for log rotation by time (daily, weekly, etc.)
        # timed_handler = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=backup_count)
        # self.logger.addHandler(timed_handler)

    def _get_caller_info(self):
        """Returns class name, method, and line number of the calling function"""
        frame = inspect.stack()[2]  # 0 is _get_caller_info, 1 is calling log method, 2 is the log caller
        module = inspect.getmodule(frame[0])
        class_name = module.__name__ if module else 'Unknown'
        method_name = frame.function
        line_number = frame.lineno
        return class_name, method_name, line_number

    def _get_datetime(self):
        """Returns current date and time in a readable format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_info(self, message: str):
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.GREEN + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}' + Style.RESET_ALL)

    def log_debug(self, message: str):
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.debug(Fore.CYAN + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}' + Style.RESET_ALL)

    def log_warning(self, message: str):
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.warning(Fore.YELLOW + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}' + Style.RESET_ALL)

    def log_error(self, message: str):
        class_name, method_name, line_number = self._get_caller_info()
        error_trace = traceback.format_exc()
        self.logger.error(Fore.RED + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}\n{error_trace}' + Style.RESET_ALL)

    def log_critical(self, message: str):
        class_name, method_name, line_number = self._get_caller_info()
        critical_trace = traceback.format_exc()
        self.logger.critical(Fore.MAGENTA + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}\n{critical_trace}' + Style.RESET_ALL)

    def start_timer(self, log_msg: str):
        """Start timer for performance measurement"""
        self.start_time = datetime.now()
        self.logger.info(f'Start: {log_msg}')

    def end_timer(self, log_msg: str):
        """End timer and log the elapsed time"""
        if hasattr(self, 'start_time'):
            elapsed_time = datetime.now() - self.start_time
            self.logger.info(f'End: {log_msg} | Elapsed Time: {elapsed_time}')
        else:
            self.logger.warning("Timer was not started before calling end_timer!")

    def set_level(self, level: str):
        """Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"""
        level_dict = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self.logger.setLevel(level_dict.get(level.upper(), logging.INFO))

    def log_exception(self, message: str, exc: Exception):
        """Log an exception with traceback"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.error(Fore.RED + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): {message}\nException: {exc}\n{traceback.format_exc()}' + Style.RESET_ALL)

# Example Usage
if __name__ == "__main__":
    logger = CustomLogger("TestLogger", log_to_file=True, log_file="custom_app.log")

    logger.log_info("This is an info message.")
    logger.log_debug("This is a debug message.")
    logger.log_warning("This is a warning message.")

    try:
        1 / 0  # Intentional error
    except Exception as e:
        logger.log_error("An error occurred.")
    
    try:
        int("invalid")  # Another error
    except Exception as e:
        logger.log_critical("A critical error occurred.")

    # Example of performance logging
    logger.start_timer("Starting heavy process")
    # Simulate some processing...
    logger.end_timer("Heavy process completed.")
