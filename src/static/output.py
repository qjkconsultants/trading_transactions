import calendar
import time
import hashlib
import os.path
import pdb
from pprint import pprint
from src.config.config import (OUTPUT_DIR, OUTPUT_DIR_PID, OUTPUT_DIR_SUMMARY_REPORT)
from src.common.utils import bcolors, print_done_message
from src.modules.transactions import Transaction
import logging
logger = logging.getLogger(__name__)

"""
This class will generate the output after receiving data from the Input class.
"""
class OutputFile:
    @staticmethod
    def get_output_file_name(input_file_name, output_file_name):
        if output_file_name:
            output_file_name = f"""{OUTPUT_DIR_SUMMARY_REPORT}{output_file_name}"""
        else:
            output_file_name = f"""{OUTPUT_DIR_SUMMARY_REPORT}out_{input_file_name}.csv"""
        return output_file_name
    
    @staticmethod
    def generate_output_files(summary_output_dict, output_file_name=None):
        OutputFile.create_directories()
        for key, summary_report in summary_output_dict.items():
            input_file_name = summary_output_dict[key].filename
            output_file_name = OutputFile.get_output_file_name(input_file_name, output_file_name)
            header_output_file = ','.join(summary_output_dict[key].output_header)
            print(f"{bcolors.GREEN}Generating Output: {output_file_name}{bcolors.ENDC}")
            with open(output_file_name, 'w') as output_file:
                output_file.write(f"""{header_output_file}\n""")
                for product_info in summary_output_dict[key].info_dict:
                    for client_info in summary_output_dict[key].info_dict[product_info]:
                        total_transaction_amount = summary_output_dict[key].info_dict[product_info][client_info]['net_total']
                        output_file.write(f"""{product_info}, {client_info}, {total_transaction_amount},\n""")
                        logger.info(f"""{product_info}, {client_info}, {total_transaction_amount},""")
        print_done_message()
    

    @staticmethod
    def create_directories():
        try:
            if not os.path.exists(OUTPUT_DIR):
                logger.info(f"""Creating output directory: {OUTPUT_DIR}""")
                os.mkdir(OUTPUT_DIR)
        except OSError as e:
            logger.info(f"""Creating output directory: {OUTPUT_DIR_PID} Failed.""")
            sys.exit("Can't create {dir}: {err}".format(dir=OUTPUT_DIR, err=e))
    
        try:
            if not os.path.exists(OUTPUT_DIR_PID):
                logger.info(f"""Creating output directory: {OUTPUT_DIR_PID}""")
                os.mkdir(OUTPUT_DIR_PID)
        except OSError as e:
            logger.info(f"""Creating output directory: {OUTPUT_DIR_PID} Failed.""")
            sys.exit("Can't create {dir}: {err}".format(dir=OUTPUT_DIR_PID, err=e))
    
        try:
            if not os.path.exists(OUTPUT_DIR_SUMMARY_REPORT):
                logger.info(f"""Creating output directory: {OUTPUT_DIR_SUMMARY_REPORT} Failed.""")
                os.mkdir(OUTPUT_DIR_SUMMARY_REPORT)
        except OSError as e:
            sys.exit("Can't create {dir}: {err}".format(dir=OUTPUT_DIR_SUMMARY_REPORT, err=e))


