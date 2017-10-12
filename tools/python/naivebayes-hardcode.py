import argparse
import csv

class CLI:
    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Analyze csv file and apply naive bayes')
        parser.add_argument('-i','--input', nargs=1, help='CSV input file')
        parser.add_argument('-c','--cache', nargs=1, help='Cache calculated probabilities to a file')
        parser.add_argument('-l','--loadcache', nargs=1, help='Load cached probabilities from file')
        parser.add_argument('-t','--test', nargs=1, help='Load test sentences from CSV file')
        parser.add_argument('-o','--out', nargs=1, help='Output test result to CSV file or -- for stdout')
        parser.add_argument('-f','--frequency', nargs=1, help='Show word frequency')
        parser.add_argument('-r','--ratio', nargs=1, 
                help='e.g. ê occurs 1000 in FR and 1 in SP, then if 1/1000 < r, remove it from SP')
        parser.add_argument('-s','--strict', action='store_true', 
                help='If a character is only available in one category then guess this category')
        args = parser.parse_args()

        # Create a naive bayes instance
        naiveBayes = NaiveBayes(args.strict)

        # Ratio
        ratio = 0

        # Checkfor missing arguments
        if args.input is None and args.loadcache is None:
            print("Missing arguments")
            exit(1)

        # Update ratio
        if args.ratio is not None:
            ratio = float(args.ratio[0])

        # Log some information
        if ratio > 0:
            print(">> Ratio value:",ratio)
        if args.strict is True:
            print(">> Strict mode enabled")

        # Load input csv
        if args.input is not None:
            print(">> Loading:", args.input[0])
            with open(args.input[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                naiveBayes.m_totalUtt = 0
                for row in reader:
                    # Increment total utt
                    naiveBayes.m_totalUtt += 1

                    # Load attributes
                    id = row['Id']
                    category = row['Category']
                    text = row['Text']

                    # Tokenize text
                    tokens = text.split()
                    for token in tokens:

                        # Init first dimension
                        if token not in naiveBayes.m_wordGivenCategoryCounter:
                            naiveBayes.m_wordGivenCategoryCounter[token] = {}

                        # Init second dimension
                        if category not in naiveBayes.m_wordGivenCategoryCounter[token]:
                            naiveBayes.m_wordGivenCategoryCounter[token][category] = 0

                        # Increment counter
                        naiveBayes.m_wordGivenCategoryCounter[token][category] += 1


                    # Init category counter
                    if category not in naiveBayes.m_categoryCounter:
                        naiveBayes.m_categoryCounter[category] = 0

                    # Increment category counter
                    naiveBayes.m_categoryCounter[category] += 1

                    # Init words per category counter
                    if category not in naiveBayes.m_wordsInCategoryCounter:
                        naiveBayes.m_wordsInCategoryCounter[category] = 0

                    # Increment words in category
                    naiveBayes.m_wordsInCategoryCounter[category] += len(tokens)
            
            # Filter counters using the ratio value
            if ratio > 0:
                naiveBayes.applyRatio(ratio)

            # Compute probabilities
            naiveBayes.compute()

        # Print word frequency
        if args.frequency is not None and args.input is not None:
            # Show stats
            print(">> Printing word frequency of words occurring in {} category to stdout".format(args.frequency[0]))
            debug = []
            for w in naiveBayes.m_wordGivenCategoryCounter:
                if len(naiveBayes.m_wordGivenCategoryCounter[w]) == int(args.frequency[0]):
                    for c in naiveBayes.m_wordGivenCategoryCounter[w]:
                        debug.append({'word': w, 'count': naiveBayes.m_wordGivenCategoryCounter[w][c], 'category':c})
            debug.sort(key=lambda x: x['count'], reverse=True)
            for object in debug:
                print("Word {} orrcurs {} in {}".format(object['word'], object['count'], object['category']))

        # Load cached probabilities
        if args.loadcache is not None:
            print(">> Loading probabilities from cache:", args.loadcache[0])
            with open(args.loadcache[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    
                    # CSV attribute
                    word = row['Word']
                    category = row['Category']
                    probability = row['Probability']
                    type = row['Type']
                    
                    # Load probability
                    if type == "word":
                        if word not in naiveBayes.m_pWordGivenCategory:
                            naiveBayes.m_pWordGivenCategory[word] = {}
                        naiveBayes.m_pWordGivenCategory[word][category] = float(probability)
                    elif type == "category":
                        naiveBayes.m_pCategory[category] = float(probability)

        # Cache probabilities
        if args.cache is not None:
            print(">> Caching computed probabilities at:", args.cache[0])
            cacheFile = open(args.cache[0], 'w')
            cacheFile.write("Word,Category,Probability,Type\n")

            # Write probability of categories
            for category in naiveBayes.m_pCategory:
                cacheFile.write(",{},{},category\n".format(category, naiveBayes.m_pCategory[category]))

            # Write probability of words
            for word in naiveBayes.m_pWordGivenCategory:
                for category in naiveBayes.m_pWordGivenCategory[word]:
                    cacheFile.write("{},{},{},word\n".format(word, category, naiveBayes.m_pWordGivenCategory[word][category]))
            cacheFile.close()

        # Prepare output
        output = "Id,Category\n"

        if args.test is not None:
            print(">> Evaluating test file:", args.test[0])
            with open(args.test[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    # Read csv attributes
                    id = row['Id']
                    text = row['Text']
                    
                    # Add output to csv
                    predict = naiveBayes.getCategory(text)
                    output += "{},{}\n".format(id, predict)

        # Process output
        if args.out is not None:
            if args.out[0] == "__":
                print(">> Printing output to stdout")
                print(output)
            else:
                print(">> Saving output to:",args.out[0])
                outputFile = open(args.out[0], 'w')
                outputFile.write(output)
                outputFile.close()

class NaiveBayes:
    def __init__(self, strict):
        """Initialize naive bayes variables"""
        
        # Set strict mode
        self.m_strict = strict

        # Total utterances
        self.m_totalUtt = 0

        # Count the number of utterances in each category
        self.m_categoryCounter= {}

        # Count the occurrence of a word in each category (e.g. var[word][cat])
        self.m_wordGivenCategoryCounter = {}

        # Count the number of words in each category
        self.m_wordsInCategoryCounter = {}

        # Store probability of a word given a category (e.g. var[word][cat])
        self.m_pWordGivenCategory = {}

        # Store the probility of a category
        self.m_pCategory = {}

        # Hardcoded
        self.m_categoryMap = {}
        # -f 1
        self.m_categoryMap["ę"] = '4'
        self.m_categoryMap["ł"] = '4'
        self.m_categoryMap["ś"] = '4'
        self.m_categoryMap["ą"] = '4'
        self.m_categoryMap["ž"] = '0'
        self.m_categoryMap["č"] = '0'
        self.m_categoryMap["ť"] = '0'
        self.m_categoryMap["ý"] = '0'
        self.m_categoryMap["ď"] = '0'
        self.m_categoryMap["ź"] = '4'
        self.m_categoryMap["ň"] = '0'
        self.m_categoryMap["ğ"] = '2'
        self.m_categoryMap["ÿ"] = '2'
        self.m_categoryMap["ŝ"] = '4'

        # -f 2
        self.m_categoryMap["ã"] = '2'
        self.m_categoryMap["ê"] = '1'
        self.m_categoryMap["¿"] = '2'
        self.m_categoryMap["¡"] = '2'
        self.m_categoryMap["ć"] = '4'
        self.m_categoryMap["š"] = '0'
        self.m_categoryMap["ñ"] = '2'
        self.m_categoryMap["û"] = '1'
        #self.m_categoryMap["ù"] = '1'
        self.m_categoryMap["ľ"] = '0'
        #self.m_categoryMap["ń"] = '4'
        #self.m_categoryMap["œ"] = '1'
        #self.m_categoryMap["ï"] = '1'
        #self.m_categoryMap["ë"] = '1'

        # -f 3
        self.m_categoryMap["è"] = '1'
        #self.m_categoryMap["ü"] = '3'
        #self.m_categoryMap["ß"] = '3'
        #self.m_categoryMap["î"] = '1'

        # -f 4
        self.m_categoryMap["à"] = '1'
        self.m_categoryMap["ç"] = '1'
        self.m_categoryMap["ö"] = '3'
        #self.m_categoryMap["ä"] = '3'

    def getCategory(self, text):
        """Conclude category from the probabilities"""

        tokens = text.split()
        result = -1
        max = -1
        for category in self.m_pCategory:
            val = self.m_pCategory[category]
            for token in tokens:
                if token in self.m_categoryMap:
                    return self.m_categoryMap[token]
                # Otherwise, proceed with the production
                if token in self.m_pWordGivenCategory:
                    val *= self.m_pWordGivenCategory[token][category]
            # Argmax of production
            if val >= max:
                max = val
                result = category
        return result

    def applyRatio(self, ratio):
        """Apply ratio"""

        for token in self.m_wordGivenCategoryCounter:
            deleteCategories = set()
            # Check if category1/category2 < ratio, then mark it to delete
            for category1 in self.m_wordGivenCategoryCounter[token]:
                for category2 in self.m_wordGivenCategoryCounter[token]:
                    if category1 != category2 \
                            and self.m_wordGivenCategoryCounter[token][category1] / \
                            self.m_wordGivenCategoryCounter[token][category2] < ratio:
                                deleteCategories.add(category1)
            # Delete tokens in categories and update the number of words in category
            if len(deleteCategories) > 0:
                print(">>>> Word {} is currently in categories {}".format( 
                        token, self.m_wordGivenCategoryCounter[token]))
            for key in deleteCategories:
                print(">>>>>> Removing word {} from category {}"
                        .format(token, key, self.m_wordGivenCategoryCounter[token][key]))
                self.m_wordsInCategoryCounter[key] -= self.m_wordGivenCategoryCounter[token][key]
                self.m_wordGivenCategoryCounter[token].pop(key)

    def compute(self):
        """Compute probabilities"""

        BIAS = 1
        print(">> Computing P(Wi|Cj)")
        for word in self.m_wordGivenCategoryCounter:

            # Init word probability
            if word not in self.m_pWordGivenCategory:
                self.m_pWordGivenCategory[word] = {}

            # Compute probabilities
            for category in self.m_categoryCounter:
                nominator = 0
                if category in self.m_wordGivenCategoryCounter[word]:
                    nominator = self.m_wordGivenCategoryCounter[word][category]
                self.m_pWordGivenCategory[word][category] = (BIAS + nominator) / \
                        (self.m_wordsInCategoryCounter[category] + len(self.m_wordGivenCategoryCounter))

        print(">> Computing P(Cj)")
        for category in self.m_categoryCounter:
            self.m_pCategory[category] = self.m_categoryCounter[category] / self.m_totalUtt

# Stat application
cli = CLI()
cli.read()
