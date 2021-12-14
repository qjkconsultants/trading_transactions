import os
import pdb
import numpy
import hashlib
import pandas
import logging
logger = logging.getLogger(__name__)

from src.modules.specifications import TransactionSpecification
from src.common.utils import (has_key, check_decimal_amount, validate_value)

"""
The class Transaction uses TransactionSpecification as parent class and inherit the properties/attributes.
The main job of the Transaction class is to parse the transactions provied in the input file.
Panda library is used to read the input from the fixed width class and it generates the datafram which is then further used to 
process the requested business logic.
"""

class Transaction(TransactionSpecification):
    def __init__(self, directory, filename):
        logger.info(f"""Initializing the super class: {TransactionSpecification}""")
        TransactionSpecification.__init__(self, directory, filename)
        logger.info(f"""Parsing the input file: {directory}/{filename}""")
        self.parse()

    def parse(self):
        dataframe = pandas.read_fwf(self.full_path, self._colspecs, names=self._header_daily_summary_report)
        self.parse_rows(dataframe)

    def parse_rows(self, dataframe):
        logger.info(f"""Processing the Transaction Row""")
        dataframe_rows = dataframe.dropna(how="all")  # remove rows that don't have any value
        dataframe_rows = dataframe_rows.replace(numpy.nan, "", regex=True)
        for index, row in dataframe_rows.iterrows():

            try:
                for k in row.keys():
                    if type(row[k]) == str:
                        row[k] = row[k].strip()
            except TypeError:  
                logger.error(f"""Issue parsing the transaction row. Line number: {index+1} | Row: {row}.""")
                raise TypeError(f"""Issue parsing the transaction row. Line number: {index+1} | Row: {row}""") 

            transaction_row = TransactionRow(
                row["record_code"], ##315
                row["client_type"], #CL
                row["client_number"], #4321
                row["account_number"], #2
                row["sub_account_number"], #1
                row["opposite_party_code"], #SGXDC
                row["product_group_code"], #FU
                row["exchange_code"], #SGX
                row["symbol"], #NK
                row["expiration_date"], #20100910
                row["currency_code"], #JPY
                row["movement_code"], #1
                row["buy_sell_code"], #B
                row["quantity_long_sign"], #
                row["quantity_long"], #1
                row["quantity_short_sign"], #
                row["quantity_short"], #0
		index
            )
            self.__add_datarow(transaction_row)

    def __add_datarow(self, row):
        if has_key(self.info_dict[row.product_information][row.client_information], 'net_total'):
            self.info_dict[row.product_information][row.client_information]['net_total'] += row.total_per_transaction
        else:
            self.info_dict[row.product_information][row.client_information]['net_total'] = row.total_per_transaction
        self._add_to_log(row.product_information, row.client_information, row.total_per_transaction)

    def _add_to_log(self, product_information, client_information, total_per_transaction):
        message = f"""Adding Net Total for the Product per Client Product: {product_information} | """
        message += f"""Client: {client_information} | Total Per Transaction: {total_per_transaction} | """
        message += f"""Net Total: {self.info_dict[product_information][client_information]['net_total']}"""
        logger.info(message)
	    
"""
TransactionRow class takes the input fields and use them to generate the desired output fields.

The CSV has the following Headers
- Client_Information
- Product_Information
- Total_Transaction_Amount

Client_Information should be a combination of the CLIENT TYPE, CLIENT NUMBER, ACCOUNT NUMBER, SUBACCOUNT NUMBER fields from Input file

Product_Information should be a combination of the EXCHANGE CODE, PRODUCT GROUP CODE, SYMBOL, EXPIRATION DATE

Total_Transaction_Amount should be a Net Total of the (QUANTITY LONG - QUANTITY SHORT) values for each client per product

"""

class TransactionRow():
    def __init__(
        self,
        record_code,
        client_type,
        client_number,
        account_number,
        sub_account_number,
        opposite_party_code,
        product_group_code,
        exchange_code,
        symbol,
        expiration_date,
        currency_code,
        movement_code,
        buy_sell_code,
        quantity_long_sign,
        quantity_long,
        quantity_short_sign,
        quantity_short,
	line_number
    ):
        self.record_code = str(record_code)
        self.client_type = str(client_type)
        self.client_number = str(client_number)
        self.account_number = str(account_number)
        self.sub_account_number = str(sub_account_number)
        self.exchange_code = str(exchange_code)
        self.product_group_code = str(product_group_code)
        self.symbol = str(symbol)
        self.expiration_date = str(expiration_date)
        self.line_number = int(line_number) + 1
        self.quantity_long = check_decimal_amount(quantity_long)
        self.quantity_short = check_decimal_amount(quantity_short)
        self.client_information = self._generate_client_information()
        self.product_information = self._generate_product_information()
        self.total_per_transaction = self._get_total_per_transaction()
        validate_value(self.record_code, "Record Code should be 315", ["315"], self.line_number)
        validate_value(self.client_number, "Client Number should be 1234 or 4321", ["1234", "4321"], self.line_number)

    def _generate_client_information(self):
        return f"""{self.client_type}_{self.client_number}_{self.account_number}_{self.sub_account_number}"""	

    def _generate_product_information(self):
        return f"""{self.exchange_code}_{self.product_group_code}_{self.symbol}_{self.expiration_date}"""	

    def _get_total_per_transaction(self):
        return check_decimal_amount(self.quantity_long - self.quantity_short)
