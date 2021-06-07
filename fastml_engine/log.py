import os
import sys
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler


class Logger:

    def __init__(self, log_path="/opt/logs", log_file_name="app.log"):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 配置输出日志格式
        log_format = "%(asctime)s\t%(levelname)s\t%(process)d\t%(thread)d\t%(module)s\t%(funcName)s\t[%(lineno)d]\t%(message)s"
        level = logging.INFO
        self.root = logging.getLogger()
        self.root.setLevel(level)
        formatter = logging.Formatter(
            fmt=log_format
        )
        if not self.root.handlers:
            fileHandler = ConcurrentRotatingFileHandler(filename=os.path.join(log_path, log_file_name),
                                                        maxBytes=50 * 1024 * 1024, backupCount=10)
            fileHandler.setLevel(level)
            fileHandler.setFormatter(formatter)

            consoleHandler = logging.StreamHandler(stream=sys.stdout)
            consoleHandler.setFormatter(formatter)
            consoleHandler.setLevel(level)

            self.root.addHandler(fileHandler)
            self.root.addHandler(consoleHandler)

    def getLogger(self, name, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger
