import logging
from logging.handlers import QueueHandler, QueueListener
import time
from khlbot.config import LOGGING_CONSOLE_LEVEL, LOGGING_FILE_LEVEL, LOGGING_FILE_DIR
import sys
import os


class Logger:
    """
    Config logging module
    """

    @staticmethod
    def listener_configure(_queue, dirpath=LOGGING_FILE_DIR, log_level=LOGGING_CONSOLE_LEVEL) -> QueueListener:
        """
        Configuration log queue listener
        :param _queue: Log queue
        :param dirpath: The path used to save log file
        :param log_level: Log level
        :return: QueueListener object
        """
        logger = logging.getLogger()
        logger.setLevel(log_level)

        formatter = logging.Formatter(f"%(asctime)s Process-%(process)s %(processName)s [%(levelname)s] : %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(log_level)
        streamHandler.setFormatter(formatter)

        listener = None
        try:
            os.makedirs(dirpath, exist_ok=True)
            fileHandler = logging.FileHandler(dirpath + f"twprgbot_{int(time.time())}.log")
            fileHandler.setLevel(log_level)
            fileHandler.setFormatter(formatter)

            listener = QueueListener(_queue, streamHandler, fileHandler)
        except Exception as err:
            logging.error(err)
            logging.warning("Logging file cannot be created, will just print log to terminal")

            listener = QueueListener(_queue, streamHandler)

        logger.addHandler(QueueHandler(queue=_queue))

        return listener

    @staticmethod
    def worker_configure(_queue, log_level=LOGGING_CONSOLE_LEVEL) -> None:
        """
        Configure logger for worker process
        :param _queue: Log queue
        :param log_level: Log level
        """
        logger = logging.getLogger()
        logger.addHandler(QueueHandler(_queue))
        logger.setLevel(log_level)

    @staticmethod
    def info(text, *args, **kwargs):
        logging.info(text, *args, **kwargs)

    @staticmethod
    def warning(text, *args, **kwargs):
        logging.warning(text, *args, **kwargs)

    @staticmethod
    def error(error: Exception, *args, **kwargs):
        tb = sys.exc_info()[2]
        logging.error(error.with_traceback(tb), *args, **kwargs)

    @staticmethod
    def debug(text, *args, **kwargs):
        logging.debug(text, *args, **kwargs)
