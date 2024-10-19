import datetime
import inspect
import logging
import sys
import time
import os
import traceback

class CustomLogger(logging.Logger):
    """
    This class is use to add custome define logger

    Args:
        logging (_type_): _description_
    """
    
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        
    def info(self, msg, *args, **kwargs):
        """
        this function is use to log the debug messege
        """  
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} INFO: {msg}"
        super().info(msg, *args, **kwargs)
        
    def debug(self, msg, *args, **kwargs):
        """
        This Function is use to Log the Debug msg
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} DEBUG: {msg}"
        super().info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """
        This Function is use to Log the Warning msg
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} WARNING: {msg}"
        super().info(msg, *args, **kwargs)
        
    def error(self, msg, *args, **kwargs):
        """
        This Function is use to Log the Error msg
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        _, _, exc_traceback = sys.exc_info()
        if exc_traceback:
            file_name, line_number, func_name, context= traceback.extract_tb(exc_traceback)[-1]
            msg += f"\n Exception in{file_name}, Line {line_number}, in {func_name}: {context}"
            
        file_name, line_num = self.__get_call_info()
        msg = f"{file_name} {line_num} : {timestamp} ERROR: {msg}"
        super().info(msg, *args, **kwargs)
        
    @staticmethod
    def shutdown():
        """
        This function is use to shutdown the logging
        """
        logging.shutdown()
        
    def __get_call_info(self):
        stack = inspect.stack()
        
        # stack[1] gives privious function ("info" in our case)
        # stack [2] goves before privious function and so on
        
        file_name = stack[2][1]
        line_num = stack[2][2]
        # func = stack[2][3]
        
        return file_name, line_num
    

class CaptureConsoleLogs:
    """
    this class have function to capture the console log
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
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            log_file_name = f'{log_file_name}_{timestamp}.log'
            cls._shared_logger = cls.setup_logger(log_file_name)
            cls._log_file_name =  log_file_name
            
        return cls._shared_logger
    
    @classmethod
    def setup_logger(cls, log_file_name):
        """
        this function sets up the logger for the file handler and console handeler

        Args:
            log_file_name (_type_): _description_
        """
        if cls._shared_logger is not None:
            return cls._shared_logger
        logger = CustomLogger("custom_logger", logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        file_hendler = logging.FileHandler(log_file_name)
        file_hendler.setLevel(logging.DEBUG)
        console_hendler = logging.StreamHandler()
        console_hendler.setLevel(logging.DEBUG)
        logger.addHandler(file_hendler)
        logger.addHandler(console_hendler)
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
        This function acts as count down timer

        Args:
            duration (_type_): _description_
        """
        while duration:
            minutes, secs = divmod(duration, 60)
            timer = f'{minutes} min :{secs} secs'
            if duration % 10 == 0:
                self.get_logger().info(f"Wait for: {timer}")
            time.sleep(1)
            duration -= 1

            
    