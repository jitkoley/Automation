import datetime
import inspect
import logging
import sys
import time
import os
import traceback

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

class CustomLogger(logging.Logger):
    """
    This class is used to add custom-defined logger
    """

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        
    def info(self, msg, *args, **kwargs):
        """
        This function is used to log the info message
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} INFO: {msg}"
        super().info(msg, *args, **kwargs)
        
    def debug(self, msg, *args, **kwargs):
        """
        This function is used to log the debug message
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} DEBUG: {msg}"
        super().info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """
        This function is used to log the warning message
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} WARNING: {msg}"
        super().info(msg, *args, **kwargs)
        
    def error(self, msg, *args, **kwargs):
        """
        This function is used to log the error message
        """
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
        """
        This function is used to shut down the logging
        """
        logging.shutdown()
        
    def __get_call_info(self):
        stack = inspect.stack()
        file_name = stack[2][1]
        line_num = stack[2][2]
        return file_name, line_num


class CaptureConsoleLogs:
    """
    This class has functions to capture console logs
    """
    _shared_logger = None
    _log_file_name = None
    _created_loggers = {}
    
    @classmethod
    def get_logger(cls):
        """
        This function returns the logger for logging
        """
        log_file_name = 'test_console'
        if cls._shared_logger is None and log_file_name not in cls._created_loggers:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            log_file_name = f'{log_file_name}_{timestamp}.log'
            cls._shared_logger = cls.setup_logger(log_file_name)
            cls._log_file_name =  log_file_name
            
        return cls._shared_logger
    
    @classmethod
    def setup_logger(cls, log_file_name):
        """
        This function sets up the logger with a file handler and console handler
        """
        if cls._shared_logger is not None:
            return cls._shared_logger

        logger = CustomLogger("custom_logger", logging.DEBUG)
        logger.setLevel(logging.DEBUG)

        # File handler (no color formatting)
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)

        # Console handler (color formatting)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = CustomFormatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        # Add both handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._shared_logger = logger
        return logger
    
    @classmethod
    def get_log_file_name(cls):
        """
        This function returns the log file name
        """
        if cls._log_file_name is not None:
            return cls._log_file_name
        return None
    
    def count_down(self, duration):
        """
        This function acts as countdown timer

        Args:
            duration (_type_): duration in seconds
        """
        while duration:
            minutes, secs = divmod(duration, 60)
            timer = f'{minutes} min :{secs} secs'
            if duration % 10 == 0:
                self.get_logger().info(f"Wait for: {timer}")
            time.sleep(1)
            duration -= 1
