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

# ANSI escape codes for colors
class ConsoleColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

class JSONFormatter(logging.Formatter):
    """Formatter for structured JSON logging."""
    
    def format(self, record):
        log_record = {
            'time': datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
            'level': record.levelname,
            'file': record.pathname,
            'line': record.lineno,
            'message': record.msg,
            'epoch': getattr(record, 'epoch', None),
            'batch': getattr(record, 'batch', None),
            'accuracy': getattr(record, 'accuracy', None),
            'loss': getattr(record, 'loss', None)
        }
        return json.dumps(log_record)


class CustomLogger(logging.Logger):
    """
    Custom logger for tracking data science project steps.
    """

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def info(self, msg, *args, **kwargs):
        epoch = kwargs.pop('epoch', None)
        batch = kwargs.pop('batch', None)
        accuracy = kwargs.pop('accuracy', None)
        loss = kwargs.pop('loss', None)

        record = self.makeRecord(self.name, logging.INFO, *inspect.stack()[1][1:3], msg, args, None, None)
        record.epoch = epoch
        record.batch = batch
        record.accuracy = accuracy
        record.loss = loss
        self.handle(record)

    def debug(self, msg, *args, **kwargs):
        self._log_with_color(logging.DEBUG, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log_with_color(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        _, _, exc_traceback = sys.exc_info()
        if exc_traceback:
            file_name, line_number, func_name, context = traceback.extract_tb(exc_traceback)[-1]
            msg += f"\n Exception in {file_name}, Line {line_number}, in {func_name}: {context}"

        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} ERROR: {msg}"
        super().info(msg, *args, **kwargs)

    def _log_with_color(self, level, msg, *args, **kwargs):
        color = {
            logging.DEBUG: ConsoleColors.OKBLUE,
            logging.INFO: ConsoleColors.OKGREEN,
            logging.WARNING: ConsoleColors.WARNING,
            logging.ERROR: ConsoleColors.FAIL,
        }.get(level, ConsoleColors.ENDC)

        msg = f"{color}{msg}{ConsoleColors.ENDC}"
        self.log(level, msg, *args, **kwargs)

    def __get_call_info(self):
        stack = inspect.stack()
        file_name = stack[2][1]
        line_num = stack[2][2]
        return file_name, line_num


class CaptureLogs:
    _shared_logger = None
    _log_file_name = None
    _created_loggers = {}
    queue_listener = None

    @classmethod
    def get_logger(cls, log_file_name='data_science', log_level=logging.DEBUG, structured_logging=True):
        """
        This function returns the logger instance for logging during data science processes.
        """
        if cls._shared_logger is None and log_file_name not in cls._created_loggers:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            log_file_name = f'{log_file_name}_{timestamp}.log'
            cls._shared_logger = cls.setup_logger(log_file_name, log_level, structured_logging)
            cls._log_file_name = log_file_name
            
        return cls._shared_logger

    @classmethod
    def setup_logger(cls, log_file_name, log_level=logging.DEBUG, structured_logging=True):
        """
        Sets up the logger with file and console handlers for tracking training and evaluation metrics.
        """
        if cls._shared_logger is not None:
            return cls._shared_logger

        logger = CustomLogger("data_science_logger", log_level)

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

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(log_level)

        # Add handlers to logger
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


# Example Usage for Data Science Workflow:

if __name__ == "__main__":
    logger = CaptureLogs.get_logger()

    # Example log for tracking dataset info
    dataset_size = 50000
    logger.info(f"Loaded dataset with {dataset_size} samples")

    # Example log for tracking model training
    for epoch in range(10):
        for batch in range(100):
            loss = 0.05 * (100 - batch)  # Simulated loss
            accuracy = 0.9 + (0.01 * batch)  # Simulated accuracy
            logger.info(f"Epoch {epoch}, Batch {batch}, Loss: {loss}, Accuracy: {accuracy}", 
                        epoch=epoch, batch=batch, loss=loss, accuracy=accuracy)

    # Example log for errors
    try:
        1 / 0  # Simulated error
    except Exception as e:
        logger.error(f"Error occurred: {e}")

    # Shutdown the logger
    CaptureLogs.shutdown_logger()
