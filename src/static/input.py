import calendar
import time
import hashlib
import os.path
import pdb
from pprint import pprint
from src.config.config import (PID)
from src.common.utils import print_start_message, bcolors
from src.modules.transactions import Transaction
import logging
logger = logging.getLogger(__name__)

class InputFile:
    @staticmethod
    def process_input_files_in_directory(input_file_directory):
        exchange_files = InputFile.list_files(input_file_directory)
        summary_output_dict, errors = InputFile.parse_input_files(input_file_directory, exchange_files)
        return (summary_output_dict, errors)
    
    @staticmethod
    def process_input_file(input_file_directory, input_file):
        exchange_files = [input_file]
        summary_output_dict, errors = InputFile.parse_input_files(input_file_directory, exchange_files)
        return (summary_output_dict, errors)

    @staticmethod
    def list_files(dir_: str, file_name=None) -> list:
        files = []
        with os.scandir(dir_) as it:
            for entry in it:
                if not entry.name.startswith(".") and not entry.name.startswith("~") and entry.is_file():
                    files.append(entry.name)
        return files

    @staticmethod
    def parse_input_files(dir_: str, files: list) -> dict:
        print_start_message("foreign exchange files", PID)
        records = {}
        counter = 1
        errors = []
        for file in files:
            print(f"Parsing {counter} of {len(files)} files from {bcolors.BLUE}{dir_}{bcolors.ENDC}", end="\r")
            logger.info(f"""Processing the input file {dir_}/{file}""")
            if os.path.isdir(dir_ + file):
                continue
            try:
                logger.info(f"""Calling the class - TradingTransactions with the input file: {dir_}/{file}""")
                ti = Transaction(dir_, file)
                records[ti.key] = ti
            except IndexError:
                # handle exception when there is a column missing or an issue with the file.
                errors.append(new_error(f"{dir_}/{file}", "", "ERROR PARSING FILE!!!"))
                logger.error(f"""Error Parsing file {dir_}/{file}""")
            counter += 1
        print()
        return records, errors
