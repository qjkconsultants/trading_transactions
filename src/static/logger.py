import logging
import sys
import os
from src.config.config import (LOG_FILENAME, LOG_FORMAT, DEFAULT_LOG_LEVEL, LEVELS, LOG_DIRECTORY)

class Logger(object):
    loggers = set()

    @staticmethod
    def start_logging(filename=LOG_FILENAME, level=DEFAULT_LOG_LEVEL):
        Logger.create_log_directory()
        "Start logging with given filename and level."
        logging.basicConfig(filename=filename,
                            level=LEVELS[level],
                            format=LOG_FORMAT)

    @staticmethod
    def create_log_directory():
        try:
            if not os.path.exists(LOG_DIRECTORY):
                os.mkdir(LOG_DIRECTORY)
        except OSError as e:
            sys.exit("Can't create {dir}: {err}".format(dir=LOG_DIRECTORY, err=e))


