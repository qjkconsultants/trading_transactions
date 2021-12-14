from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from src.exceptions.invalid_value_exception import InvalidValueException

def check_decimal_amount(val):
    if val:
        return round(Decimal(val), 2)
    else:
        return int(0)

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

def print_start_message(type: str, process_id):
    print(f"{bcolors.BOLD}Starting {type} files comparison...{bcolors.ENDC}")
    print(f"This Process ID (process_id) is: {bcolors.GREEN}{process_id}{bcolors.ENDC}")

def print_done_message():
    print(f"{bcolors.GREEN}DONE{bcolors.ENDC}")


def has_key(dictionary, key):
    if key in dictionary.keys():
        return True
    else:
        return False

def validate_value(value, error_message, expected_values_list, line_number=None):
    if value not in expected_values_list:
        raise InvalidValueException(value, error_message, line_number)  

def check_date_format(date_text, line_number=None):
    try:
        datetime.strptime(date_text, '%Y%m%d')
        return True
    except ValueError:
        if line_number:
            raise ValueError(f"""Incorrect data format, should be YYYYMMDD and not {date_text} - Line Number: {line_number}""")
        else:
            raise ValueError(f"""Incorrect data format, should be YYYYMMDD and not {date_text}""")

# Just a few colors to use in the console logs.
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
