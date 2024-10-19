import logging
import inspect
import traceback
from logging.handlers import RotatingFileHandler
from datetime import datetime
from colorama import Fore, Style, init
import pandas as pd

# Initialize colorama for cross-platform support
init(autoreset=True)

class DataScienceLogger:
    def __init__(self, name: str, log_to_file: bool = False, log_file: str = 'data_science.log', max_file_size: int = 5 * 1024 * 1024, backup_count: int = 5):
        """
        Custom Logger for Data Science projects.
        
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

    def log_dataframe_info(self, df: pd.DataFrame, df_name: str = "DataFrame"):
        """Log the basic information of a pandas DataFrame"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.BLUE + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): DataFrame: {df_name}\n'
                                     f'Shape: {df.shape}\n'
                                     f'Columns: {list(df.columns)}\n'
                                     f'Dtypes:\n{df.dtypes}' + Style.RESET_ALL)

    def log_model_metrics(self, metrics: dict):
        """Log the model performance metrics"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.LIGHTCYAN_EX + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): Model Metrics:\n'
                                             f'{metrics}' + Style.RESET_ALL)

    def log_hyperparameters(self, params: dict):
        """Log model hyperparameters"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.LIGHTWHITE_EX + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): Model Hyperparameters:\n'
                                              f'{params}' + Style.RESET_ALL)

    def log_training_progress(self, epoch: int, loss: float, accuracy: float):
        """Log model training progress"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.LIGHTGREEN_EX + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): Epoch: {epoch}, '
                                              f'Loss: {loss}, Accuracy: {accuracy}' + Style.RESET_ALL)

    def log_data_preprocessing(self, step: str, details: str):
        """Log data preprocessing steps"""
        class_name, method_name, line_number = self._get_caller_info()
        self.logger.info(Fore.LIGHTYELLOW_EX + f'{self._get_datetime()} - {class_name}.{method_name} (Line {line_number}): '
                                               f'Data Preprocessing - {step}: {details}' + Style.RESET_ALL)

# Example Usage
if __name__ == "__main__":
    logger = DataScienceLogger("DataScienceLogger", log_to_file=True, log_file="data_science_project.log")

    logger.log_info("Starting data preprocessing...")

    # Log DataFrame info
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c'],
        'col3': [True, False, True]
    })
    logger.log_dataframe_info(df, df_name="Sample DataFrame")

    # Log hyperparameters
    hyperparams = {
        'learning_rate': 0.001,
        'batch_size': 32,
        'optimizer': 'Adam'
    }
    logger.log_hyperparameters(hyperparams)

    # Log training progress
    logger.log_training_progress(epoch=1, loss=0.25, accuracy=0.92)

    # Log model metrics
    metrics = {
        'accuracy': 0.92,
        'precision': 0.89,
        'recall': 0.87,
        'f1_score': 0.88
    }
    logger.log_model_metrics(metrics)
    
    # Simulate an error
    try:
        1 / 0
    except Exception as e:
        logger.log_error("An error occurred.")
