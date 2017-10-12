import argparse
import csv

class CLI:
    def lcs(a, b):
        lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                if x == y:
                    lengths[i+1][j+1] = lengths[i][j] + 1
                else:
                    lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
        return lengths[len(a)][len(b)]

    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Analyze csv file and apply naive bayes')
        parser.add_argument('-d','--data', nargs=1, help='Data csv file. Id,Category,Text')
        parser.add_argument('-t','--test', nargs=1, help='Test csv file. Id,Text')
        args = parser.parse_args()

        # Checkfor missing arguments
        if args.data is None or args.test is None:
            print("Missing arguments")
            exit(1)
        
        # Files entries
        dEntries = []
        tEntries = []
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
                if text not in dTextCategory:
                    dTextCategory[text] = {}
                if category not in dTextCategory[text]:
                    dTextCategory[text][category] = 0
                dTextCategory[text][category] += 1

        # Load test file
        print(">> Loading test file:", args.test[0])
        with open(args.test[0], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = row['Id']
                text = row['Text']
                tEntries.append({'id':id, 'text':text})

        # Find matches
        count = 0;
        for tEntry in tEntries:
            if tEntry['text'] in dTextCategory:
                if len(tEntry['text']) >= 20:
                    break
                count +=1
                print(tEntry['text'])
        print(count)
# Stat application
cli = CLI()
cli.read()
