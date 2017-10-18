import argparse
import csv
import collections
import math
import threading

CORES = 7

def match(longTestEntries, longTrainEntries, fromIndex, toIndex, fileName):
    # Prepare output
    print(">> Generating csv file:", fileName)
    outputFile = open(fileName, 'w')
    outputFile.write("Id,Category\n")

    # Compare entries
    progress = 0
    match = 0
    for testEntryIndex in range(fromIndex, toIndex+1):
        # Log progress
        if progress % 100 == 0:
            print(">> Completed {} out of {} long test entries, with {} matches".format(
                fromIndex + progress, toIndex, match))
        
        # Start comparing test and training entries    
        categoriesCounter = {}
        testEntry = longTestEntries[testEntryIndex]
        for trainEntry in longTrainEntries:
            missing=0
            testKeySet = set(testEntry['collections'].keys())
            trainKeySet = set(trainEntry['collections'].keys())

            # Compute intersction
            intersect = testKeySet & trainKeySet
            testKeyEx = testKeySet - intersect
            
            # Compute the dif
            for key in intersect:
                missing += max(0, testEntry['collections'][key] - trainEntry['collections'][key])
            for key in testKeyEx:
                missing += testEntry['collections'][key]

            # Increment counter if the missing characters
            # are below the threshold
            if missing <= 2:
                if trainEntry['category'] not in categoriesCounter:
                    categoriesCounter[trainEntry['category']] = 0
                categoriesCounter[trainEntry['category']] += 1
                match+=1

        # Select the best category
        selectedCategory = -1
        for tmpCategory in categoriesCounter:
            if selectedCategory == -1 or categoriesCounter[selectedCategory] < categoriesCounter[tmpCategory]:
                selectedCategory = tmpCategory

        # Write category in file
        if selectedCategory != -1:
            outputFile.write("{},{}\n".format(testEntry['id'], selectedCategory))
        progress+=1
    outputFile.close()

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

        # Create long keys
        longTestEntries = list(x for x in tEntries if len(x['text']) == 20)
        longTrainEntries = []
        for entry in dTextCategory:
            if len(entry) > 20 and len(entry) <= 21:
                longTrainEntries.append({'text': entry, 'category': dTextCategory[entry]})

        # Add collections
        for testEntry in longTestEntries:
            testEntry['collections'] = collections.Counter(testEntry['text'])
        for trainEntry in longTrainEntries:
            trainEntry['collections'] = collections.Counter(trainEntry['text'])

        # Split test for threading
        parts = list(range(0, len(longTestEntries), math.ceil(len(longTestEntries)/CORES)))

        # Create threads
        threads = []
        for i in range(len(parts)):
            fromIndex = parts[i]
            toIndex = 0
            if i == len(parts)-1:
                toIndex = len(longTestEntries)
            else:
                toIndex = parts[i+1]
            threads.append(threading.Thread(target=match, args=(
                longTestEntries, longTrainEntries, fromIndex, toIndex, 
                "{}-{}".format(args.output[0], fromIndex),)))
            threads[-1].start()

        # Join threads
        for thread in threads:
            thread.join()

# Stat application
cli = CLI()
cli.read()
