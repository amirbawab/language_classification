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
        parser.add_argument('-a','--algo', nargs='+', help='Algorithms')
        args = parser.parse_args()

        # Check for missing arguments
        if args.input is None or args.output is None:
            print("Missing arguments")
            exit(1)

        # Prepare csv variables
        entries = []

        # Load csv
        if args.input is not None:
            print(">> Loading CSV file:", args.input[0])
            with open(args.input[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id = row['Id']
                    text = row['Text']
                    entries.append({"id":id, "text": text})

        # Apply algorithms
        if args.algo is not None:
            for algo in args.algo:
                print(">> Applying algorithm:",algo)
                if algo == "no_space":
                    for entry in entries:
                        entry['text'] = "".join(entry['text'].split())
                elif algo == "sort_lex":
                    for entry in entries:
                        entry['text'] = "".join(sorted(entry['text'], key=str.lower))
                elif algo == "sort_len":
                    entries.sort(key=lambda x: len(x['text']))
                else:
                    print(">> Algorithm:",algo,"not found!")

        # Prepare output
        if args.output is not None:
            print(">> Generating CSV:", args.output[0])
            outputFile = open(args.output[0], 'w')
            outputFile.write("Id,Text\n")
            for entry in entries:
                outputFile.write("{},{}\n".format(entry['id'], entry['text']));
            outputFile.close()
            
# Stat application
cli = CLI()
cli.read()
