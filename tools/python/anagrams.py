import argparse
import csv
import math

class CLI:

    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Search for anagrams between two files')
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
        outEntries = {}

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
                outEntries[id] = -1

        # Manipulate the hash map
        # If a text key belongs to multiple categories
        # then select the category that dominates
        # and remove all the others
        print(">> Selecting the category that is the most occurring")
        for entry in dTextCategoryCounter:
            bestCategory = -1
            for category in dTextCategoryCounter[entry]:
                if bestCategory == -1 or \
                        dTextCategoryCounter[entry][bestCategory] < dTextCategoryCounter[entry][category]:
                            bestCategory = category
            dTextCategory[entry] = bestCategory

        #################################
        # Phase 1: Anagrams subsequence #
        #################################
        print(">> Starting phase 1: Anagrams Subsequence ...")

        # Create long keys
        longTestEntries = list(x for x in tEntries if len(x['text']) == 20)
        longTrainEntries = []
        for entry in dTextCategory:
            if len(entry) >= 21 and len(entry) <= 26:
                longTrainEntries.append({'text': entry, 'category': dTextCategory[entry]})

        # Compare entries
        progress = 0
        match = 0
        for testEntry in longTestEntries:
            # Log progress
            if progress % 100 == 0:
                print(">> Completed {} out of {} long test entries, with {} matches".format(
                    progress, len(longTestEntries), match))
            
            # Start comparing test and training entries    
            categoriesCounter = {}
            for trainEntry in longTrainEntries:
                testIndex = 0
                trainIndex = 0
                while testIndex < len(testEntry['text']) and trainIndex < len(trainEntry['text']):
                    if testEntry['text'][testIndex] == trainEntry['text'][trainIndex]:
                        testIndex += 1
                        trainIndex += 1
                    elif testEntry['text'][testIndex] < trainEntry['text'][trainIndex]:
                        break
                    else:
                        trainIndex += 1

                if testIndex == len(testEntry['text']):
                    if trainEntry['category'] not in categoriesCounter:
                        categoriesCounter[trainEntry['category']] = 0
                    categoriesCounter[trainEntry['category']] += 1

            # Select the best category
            selectedCategory = -1
            for tmpCategory in categoriesCounter:
                if selectedCategory == -1 or categoriesCounter[selectedCategory] < categoriesCounter[tmpCategory]:
                    selectedCategory = tmpCategory
                
            # Store selected category
            outEntries[testEntry['id']] = selectedCategory
            if selectedCategory != -1:
                match+=1
            progress+=1

        #####################################
        # Phase 2: Anagrams of equal length #
        #####################################
        print(">> Starting phase 2: Anagrams of equal length ...")

        for entry in tEntries:
            if entry['text'] in dTextCategory:
                outEntries[entry['id']] = dTextCategory[entry['text']]

        # Prepare output
        print(">> Generating csv file:", args.output[0])
        outputFile = open(args.output[0], 'w')
        outputFile.write("Id,Category\n")
        for entryId in outEntries:
            if outEntries[entryId] != -1:
                outputFile.write("{},{}\n".format(entryId, outEntries[entryId]))
        outputFile.close()

# Stat application
cli = CLI()
cli.read()
