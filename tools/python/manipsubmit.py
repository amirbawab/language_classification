import argparse
import random
import csv
import os

class CLI:
    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Apply algorithms on the csv test file. Header: Id,Text')
        parser.add_argument('-i','--input', nargs=1, help='CSV input file')
        parser.add_argument('-o','--output', nargs=1, help='CSV output file')
        parser.add_argument('-m','--merge', nargs=1, help='CSV file with values that will overwrite input file')
        args = parser.parse_args()

        # Check for missing arguments
        if args.input is None or args.output is None or args.merge is None:
            print("Missing arguments")
            exit(1)

        # Prepare csv variables
        entries = {}

        # Load input csv
        print(">> Loading input CSV file:", args.input[0])
        with open(args.input[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                category = row['Category']
                entries[id] = {"id":id, "category": category}

        # Load merge csv
        print(">> Loading merge CSV file:", args.merge[0])
        with open(args.merge[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                category = row['Category']
                entries[id]["category"] = category

        # Prepare output
        print(">> Generating CSV:", args.output[0])
        outputFile = open(args.output[0], 'w')
        outputFile.write("Id,Category\n")
        for entry in entries:
            outputFile.write("{},{}\n".format(entries[entry]['id'], entries[entry]['category']));
        outputFile.close()
            
# Stat application
cli = CLI()
cli.read()
