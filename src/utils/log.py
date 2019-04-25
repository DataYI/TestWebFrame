import logging
from logging.handlers import RotatingFileHandler
import threading
from src.config.global_value import LOG_PATH
from datetime import datetime


class Logger:
    __instance = None
    __mutex = threading.Lock()

    def __new__(cls):
        with cls.__mutex:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
                cls.__instance.__setup()
                cls.__instance.__setup_logger()
        return cls.__instance


    def __init__(self):
        pass

    
    def __setup(self):
        self.log_file = (LOG_PATH / ('%s.log' % datetime.today().strftime('%Y%m%d'))).as_posix()
        self.backup_count = 5
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.is_console_log_on = True
        self.is_file_log_on = True
        self.console_output_level = 20
        self.file_output_level = 10
        self.max_bytes = 0


    def get_logger(self):
        return self.logger


    def __setup_logger(self):
        self.logger = logging.getLogger(self.log_file)
        # 如果开启控制台日志
        if self.is_console_log_on:
            console = logging.StreamHandler()
            console.setLevel(self.console_output_level)
            console.setFormatter(self.formatter)
            self.logger.addHandler(console)
            # logger.setLevel(self.console_output_level)
        # 如果开启文件日志
        if self.is_file_log_on:
            file_handler = RotatingFileHandler(self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count)
            file_handler.setLevel(self.file_output_level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
            # logger.setLevel(self.file_output_level)


# logger = Logger().get_logger()