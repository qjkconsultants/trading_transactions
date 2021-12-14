import os
from optparse import OptionParser
from src.static.input import InputFile
from src.static.output import OutputFile
from src.static.logger import Logger as logger
from src.common.utils import print_start_message, print_done_message

"""Process Single Input File"""
def process_single_file(input_directory, input_file, output_file):
    (summary_output_dict, errors) = InputFile.process_input_file(input_directory, input_file)
    if not errors:
        OutputFile.generate_output_files(summary_output_dict, output_file)
    else: 
        print_errors(errors)

"""Process Multiple Input Files"""
def process_files_in_directory(input_directory):
    (summary_output_dict, errors) = InputFile.process_input_files_in_directory(input_directory)
    if not errors:
        OutputFile.generate_output_files(summary_output_dict)
    else: 
        print_errors(errors)

"""Print errors while parsing the input files data"""
def print_errors(errors):
    for error in errors:
        print(f"""Errors: {error}""")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--dir", action="store", type="string", dest="dir", help="Directory for the input files - python cli.py -d input_files")
    parser.add_option("-i", "--input", action="store", type="string", dest="input_file", help="Input File - Input.txt - python cli.py -d input_files -i Input.txt -o Output.csv")
    parser.add_option("-o", "--output", action="store", type="string", dest="output_file", help="Ouput File - Output.csv - python cli.py -d input_files -i Input.txt -o Output.csv")
    (options, args) = parser.parse_args()
    logger.start_logging()

    if not options.dir and options.input_file and options.output_file:
        parser.error("please provide the name of the input files directory")
    if options.dir and not options.input_file and options.output_file:
        parser.error("please provide the name of the input file")
    if options.dir and options.input_file and not options.output_file:
        parser.error("please provide the name of the output file")

    if options.dir and options.input_file and options.output_file:
        process_single_file(options.dir, options.input_file, options.output_file)

    if options.dir and not options.input_file and not options.output_file:
        process_files_in_directory(options.dir)
