import argparse
import csv
import collections

class CLI:

    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Analyze csv file and apply naive bayes')
        parser.add_argument('-d','--data', nargs=1, help='Data csv file. Id,Category,Text')
        parser.add_argument('-t','--test', nargs=1, help='Test csv file. Id,Text')
        parser.add_argument('-r','--ratio', nargs=1, help='Ratio threshold value')
        parser.add_argument('-o','--output', nargs=1, help='Output csv file')
        args = parser.parse_args()

        # Checkfor missing arguments
        if args.data is None or args.test is None or args.output is None or args.ratio is None:
            print("Missing arguments")
            exit(1)

        # Get LCS value
        ratioThresh = float(args.ratio[0])
        
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
        generated = set()
        result = "Id,Category\n"

        # Start matching
        print(">> Start matching")
        memo = {}
        progress = 0
        for entry in tEntries:
            progress += 1
            category = -1
            
            # Log progress
            if progress % 10000 == 0:
                print(">> Completed {} out of {}".format(progress, len(tEntries)))

            # Check if calculated already
            if entry['text'] in memo:
                category = memo[entry['text']]

            # Check if a complete key match is found
            elif entry['text'] in dTextCategory:
                category = dTextCategory[entry['text']]

            # Compare the characters
            else:
                categoryCounter = {}
                longKeys = (x for x in dTextCategory if len(x) >= len(entry['text']))
                for key in longKeys:

                    # Find common characters
                    matchCounter = 0
                    letters = collections.Counter(key)
                    for char in entry['text']:
                        if char in letters and letters[char] > 0:
                            letters[char] -= 1
                            matchCounter += 1

                    # Compute and compare the match ratio
                    # FIXME handle case when len(entry['text']) is 0
                    ratio = matchCounter / len(entry['text'])
                    if ratio >= ratioThresh:
                        if dTextCategory[key] not in categoryCounter:
                            categoryCounter[dTextCategory[key]] = 0
                        categoryCounter[dTextCategory[key]] += 1

                # Select the best category
                for tmpCat in categoryCounter:
                    if category == -1 or categoryCounter[tmpCat] > categoryCounter[category]:
                        category = tmpCat

                # Memo result
                memo[entry['text']] = category

            # If category found, create entry
            if category != -1:
                result += "{},{}\n".format(entry['id'], category)

        # Output
        print(">> Generating output file:", args.output[0])
        outputFile = open(args.output[0], 'w')
        outputFile.write(result)
        outputFile.close()



# Stat application
cli = CLI()
cli.read()
