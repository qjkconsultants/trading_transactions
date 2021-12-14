import os
import os.path
import calendar
import time
import hashlib
import numpy
import pandas
import logging
logger = logging.getLogger(__name__)
from src.config.config import ENCODING
from src.common.utils import nested_dict

OUTPUT_HEADER = [
   "Client_Information",
   "Product_Information",
   "Total_Transaction_Amount"
]

HEADER_DAILY_SUMMARY_REPORT = {
        "record_code": (0,3),
        "client_type": (3,7),
        "client_number": (7,11),
        "account_number": (11,15),
        "sub_account_number": (15,19),
        "opposite_party_code": (19,25),
        "product_group_code": (25,27),
        "exchange_code": (27,31),
        "symbol": (31,37),
        "expiration_date": (37,45),
        "currency_code": (45,48),
	"movement_code": (48,50),
	"buy_sell_code": (50,51),
	"quantity_long_sign": (51,52),
	"quantity_long": (52,62),
	"quantity_short_sign": (62,63),
	"quantity_short": (63,73),
	"exchange_broker_fee_dec": (73,85),
	"exchange_broker_fee_d_c": (85,86),
	"exchange_broker_fee_current_code": (86,89),
	"clearing_fee_dec": (89,101),
	"clearing_fee_d_c": (101,102),
	"clearing_fee_current_code": (102,105),
	"commission": (105,117),
	"commission_d_c": (117, 118),
	"commission_current_code": (118,121),
	"transaction_date": (121, 129),
	"future_reference": (129, 135),
	"ticket_number": (135, 141),
	"external_number": (141, 147),
	"transaction_price_dec": (147, 162),
	"trader_initials": (162, 168),
	"opposite_trader_id": (168, 175),
	"open_close_code": (175, 176),
	"filler": (176, 303),
}

def create_system_A_files_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    if not os.path.exists(OUTPUT_DIR_PID):
        os.mkdir(OUTPUT_DIR_PID)

    if not os.path.exists(OUTPUT_DIR_DAILY_SUMMARY_REPORT):
        os.mkdir(OUTPUT_DIR_DAILY_SUMMARY_REPORT)

class TransactionSpecification:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename
        self.datarows = {}
        self.info_dict = nested_dict(3, int)
        self._header_dict = HEADER_DAILY_SUMMARY_REPORT
        self._output_header = OUTPUT_HEADER
        self._header_daily_summary_report = []
        self._colspecs = []
        self.__generate_headers()
        self._key = self.__generate_key()

    @property
    def full_path(self):
        self.__fix_path()
        return self.directory + self.filename

    @property
    def key(self):
        return self._key
    
    @property
    def output_header(self):
        return self._output_header

    def __generate_key(self):
        sha = hashlib.sha256()
        sha.update(self.filename.encode(ENCODING))
        return sha.hexdigest()

    def __generate_headers(self):
        for key, value in self._header_dict.items():
            self._header_daily_summary_report.append(key)
            self._colspecs.append(value)

    def __fix_path(self):
        if self.directory[-1] != '/':
            self.directory += '/'


