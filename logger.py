import logging
import sys
from singleton import Singleton

@Singleton
class LoggerFacade:
    """
    Class representing the logger used throughout the project.
    """
    def __init__(self):
        """
        Initializes logger and sets config.
        """
        self.logger: Logger = logging.getLogger()
        file = "./logs/logfile.txt"
        
        # Clear the file before running...
        with open("./logs/logfile.txt") as f:
            f.truncate(0)

        filehandler = logging.FileHandler(f"./logs/logfile.txt", "a")
        formatter = logging.Formatter('%(asctime)-15s::%(levelname)s::%(filename)s::%(funcName)s::%(lineno)d::%(message)s')
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def info(self, msg: str):
        """
        Logs information.
        :param msg: The message.
        """
        self.logger.info(msg)

    def warning(self, msg: str):
        """
        Logs warning.
        :param msg: The message.
        """
        self.logger.warning(msg)

    def critical(self, msg: str):
        """
        Logs a critical error.
        :param msg: The message.
        """
        self.logger.critical(msg)

"""
The singleton logger used in all classes.
"""
Logger = LoggerFacade.instance()