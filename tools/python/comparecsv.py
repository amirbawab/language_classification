import argparse
import csv

class CLI:
    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(
                description='Compare and report accuracy of two csv files with header: Id,Category')
        parser.add_argument('-s','--submit', nargs=1, help='CSV test result to submit')
        parser.add_argument('-a','--answer', nargs=1, help='CSV test answer to compare against')
        args = parser.parse_args()

        # Checkfor missing arguments
        if args.submit is None or args.answer is None:
            print("Missing arguments")
            exit(1)

        # Data storage
        entries = {}

        # Load submit
        print(">> Loading submit file:",args.submit[0])
        with open(args.submit[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                category = row['Category']
                entries[id] = {"id":id, "category":category}

        # Load answer
        correct = 0
        print(">> Loading answer file:",args.answer[0])
        with open(args.answer[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                category = row['Category']
                if id in entries:
                    if entries[id]['category'] == category:
                        correct += 1
                else:
                    print("Id {} was not found in the submit file".format(id))

        # Report accuracy
        print(">> Report results")
        print("Total: {}, Correct: {}, Accuracy: {}".format(len(entries), correct, correct/len(entries)))

# Stat application
cli = CLI()
cli.read()
