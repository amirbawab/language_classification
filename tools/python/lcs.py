import argparse
import csv

def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    return lengths[len(a)][len(b)]

class CLI:

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

        # Run LCS
        memo = {}
        confidenceMemo = {}
        for entry in tEntries:
            category = -1
            confidence = -1

            # Check in memo
            if entry['text'] in memo:
                category = memo[entry['text']]
                confidence = confidenceMemo[entry['text']]

            # Find a complete match first
            elif entry['text'] in dTextCategory:
                category = dTextCategory[entry['text']]
                confidence = 1

            # Otherwise, try LCS
            else:
                bestLCS = -1
                for key in dTextCategory:
                    if len(key) >= len(entry['text']):
                        lcsRet = lcs(key, entry['text'])
                        if lcsRet > bestLCS:
                            bestLCS = lcsRet
                            category = dTextCategory[key]
                        # If best we can get, don't continue
                        if lcsRet == len(entry['text']):
                            break
                    
                # Compute confidence level
                if bestLCS == len(entry['text']):
                    confidence = 1
                else:
                    confidence = bestLCS / len(entry['text'])
                confidenceMemo[entry['text']] = confidence
                memo[entry['text']] = category
            print("[{}],{},{},{}".format(confidence, entry['id'], entry['text'], category))


# Stat application
cli = CLI()
cli.read()
