import argparse
import csv
import collections

class CLI:

    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Search for exact match between two files')
        parser.add_argument('-d','--data', nargs=1, help='Data csv file. Id,Category,Text')
        parser.add_argument('-t','--test', nargs=1, help='Test csv file. Id,Text')
        parser.add_argument('-o','--output', nargs=1, help='Output csv file')
        args = parser.parse_args()

        # Checkfor missing arguments
        if args.data is None or args.test is None or args.output is None:
            print("Missing arguments")
            exit(1)

        # Files entries
        dEntries = []
        tEntries = []
        dTextCategoryCounter = {}
        dTextCategory = {}

        # Load data file
        print(">> Loading data file:", args.data[0])
        with open(args.data[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                category = row['Category']
                text = row['Text']
                dEntries.append({'id':id, 'category':category, 'text':text})
                if text not in dTextCategoryCounter:
                    dTextCategoryCounter[text] = {}
                if category not in dTextCategoryCounter[text]:
                    dTextCategoryCounter[text][category] = 0
                dTextCategoryCounter[text][category] += 1

        # Load test file
        print(">> Loading test file:", args.test[0])
        with open(args.test[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                text = row['Text']
                tEntries.append({'id':id, 'text':text})

        # Manipulate the hash map
        # If a text key belongs to multiple categories
        # then select the category that dominates
        # and remove all the others
        for entry in dTextCategoryCounter:
            bestCategory = -1
            for category in dTextCategoryCounter[entry]:
                if bestCategory == -1 or \
                        dTextCategoryCounter[entry][bestCategory] < dTextCategoryCounter[entry][category]:
                            bestCategory = category
            dTextCategory[entry] = bestCategory

        # Prepare output
        print(">> Generating csv file:", args.output[0])
        outputFile = open(args.output[0], 'w')
        outputFile.write("Id,Category\n")

        # Start writing the entries
        for entry in tEntries:
            if entry['text'] in dTextCategory:
                outputFile.write("{},{}\n".format(entry['id'], dTextCategory[entry['text']]))
        outputFile.close()

# Stat application
cli = CLI()
cli.read()
