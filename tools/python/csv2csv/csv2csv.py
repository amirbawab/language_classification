import argparse
import csv

class CLI:
    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Merge two csv files into one')
        parser.add_argument('-t','--text', nargs=1, help='CSV text file')
        parser.add_argument('-l','--lang', nargs=1, help='CSV language file')
        parser.add_argument('-o','--out', nargs=1, help='CSV output file')
        parser.add_argument('-a','--algo', nargs='+', help='Algorithm id to be performed on the text')
        args = parser.parse_args()

        # Check for missing arguments
        if args.text is None or args.lang is None or args.out is None:
            print("Missing arguments")
            exit(1)

        # Prepare csv variables
        entries = {}

        # Load text csv
        if args.text is not None:
            print(">> Loading CSV text:", args.text[0])
            with open(args.text[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    # Load attributes
                    id = row['Id']
                    text = row['Text']
                    
                    # Add objects
                    entries[id] = {"id":id, "text": text}

        # Load lang csv
        if args.lang is not None:
            print(">> Loading CSV language:", args.lang[0])
            with open(args.lang[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    # Load attributes
                    id = row['Id']
                    category = row['Category']
                    
                    # Update objects
                    entries[id]['category'] = category

        # Prepare output
        if args.out is not None:
            print(">> Generating CSV:", args.out[0])
            outputFile = open(args.out[0], 'w')
            outputFile.write("Id,Category,Text");
            for entry in entries:
                outputFile.write("{},{},{}\n".format(entries[entry]['id'], entries[entry]['category'], 
                    entries[entry]['text']));
            outputFile.close()

# Stat application
cli = CLI()
cli.read()
