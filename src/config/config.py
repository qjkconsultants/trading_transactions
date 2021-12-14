import calendar
import time
import logging
import sys
import os

ENCODING = 'utf-8'
PID = str(calendar.timegm(time.gmtime()))
OUTPUT_DIR = './output/'
OUTPUT_DIR_PID = OUTPUT_DIR + PID + '/'
OUTPUT_DIR_SUMMARY_REPORT = OUTPUT_DIR_PID + 'trading_summary/' 
LOG_DIRECTORY="./logs"
LOG_FILENAME = f"""{LOG_DIRECTORY}/trade_transactions_summary_report_log.txt"""
LOG_FORMAT = "%(asctime)s %(name)s:%(levelname)s:%(filename)s function:%(funcName)s line:%(lineno)d %(message)s"
DEFAULT_LOG_LEVEL = "info" # Default log level
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }

