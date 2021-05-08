import logging
import time
from khlbot.config import LOGGING_CONSOLE_LEVEL, LOGGING_FILE_LEVEL
import sys


class Logger:
    """
    Config logging module
    """
    __logger = None

    @classmethod
    def init(cls):
        logger = logging.getLogger(__file__)
        logger.setLevel(LOGGING_CONSOLE_LEVEL)

        fileHandler = logging.FileHandler(f"twprgbot_{int(time.time())}.log")
        fileHandler.setLevel(LOGGING_FILE_LEVEL)

        steamHandler = logging.StreamHandler()
        steamHandler.setLevel(LOGGING_CONSOLE_LEVEL)

        formatter = logging.Formatter("%(asctime)s [%(filename)s %(lineno)d] : [%(levelname)s] %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")

        fileHandler.setFormatter(formatter)
        steamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(steamHandler)

        cls.__logger = logger

    @classmethod
    def info(cls, text, *args, **kwargs):
        if cls.__logger is not None:
            cls.__logger.info(text, *args, **kwargs)

    @classmethod
    def warning(cls, text, *args, **kwargs):
        if cls.__logger is not None:
            cls.__logger.warning(text, *args, **kwargs)

    @classmethod
    def error(cls, error: Exception, *args, **kwargs):
        if cls.__logger is not None:
            tb = sys.exc_info()[2]
            cls.__logger.error(error.with_traceback(tb), *args, **kwargs)
