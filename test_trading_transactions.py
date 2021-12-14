import unittest
import os
import glob
import pandas
import numpy
import pdb

class TestTradingTransactions(unittest.TestCase):
    def setUp(self):
        self.path = r'./input' 
        self.file_name = "Input.txt"
        self.full_path = f"""{self.path}/{self.file_name}"""

    """Length of the file excluding the filler and the new line should be 176"""
    def testRowLength(self):
        expected = 176
        with open(self.full_path, 'r') as input_file:
            lines = input_file.readlines()
        count = 0
        for line in lines:
            count += 1
            observed = len(line.rstrip())
            self.assertEqual(observed, expected, f"""File should have 176 characters excluding new line. Expected Length: {expected} - Actual Length: {observed}""")

    """Only two clients should be included in the file - client number 1234 and 4321"""
    def testClientNumber(self):
        dataframe = pandas.read_fwf(self.full_path, colspecs=[(7,11)], names=['client_number'])
        self.dataframe_rows = dataframe.dropna(how="all")  # remove rows that don't have any value
        self.dataframe_rows = self.dataframe_rows.replace(numpy.nan, "", regex=True)
        expected_client = [1234, 4321]
        for index, row in self.dataframe_rows.iterrows():
           observed = row["client_number"]
           self.assertTrue(observed in expected_client, f"""Invalid client number found in the file: {observed}. Expected clients should be one the numbers provided in the list: {expected_client}""")

    """First 3 characters of the files should be 315"""
    def testRecordCode(self):
        dataframe = pandas.read_fwf(self.full_path, colspecs=[(0,3)], names=['record_code'])
        self.dataframe_rows = dataframe.dropna(how="all")  # remove rows that don't have any value
        self.dataframe_rows = self.dataframe_rows.replace(numpy.nan, "", regex=True)
        expected = 315
        for index, row in self.dataframe_rows.iterrows():
           observed = row["record_code"]
           self.assertEqual(observed, expected, f"""First 3 characters of the record code are not correct. Expected code: {expected} - Code Found: {observed} - Line Number: {index+1}""")
	
    """Expiration Date should be CCYYMMDD"""
    def testExpirationDate(self):
        from src.common.utils import check_date_format
        dataframe = pandas.read_fwf(self.full_path, colspecs=[(37,45)], names=['expiration_date'])
        self.dataframe_rows = dataframe.dropna(how="all")  # remove rows that don't have any value
        self.dataframe_rows = self.dataframe_rows.replace(numpy.nan, "", regex=True)
        for index, row in self.dataframe_rows.iterrows():
           expiration_date = str(row["expiration_date"])
           self.assertTrue(check_date_format(expiration_date, index+1), f"""Expiration date format is not CCYYMMDD. Date format found: {expiration_date} - Line Number: {index+1}""")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

