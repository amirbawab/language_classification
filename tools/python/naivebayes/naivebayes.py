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
        parser.add_argument('-s','--sentence', nargs=1, help='Sentence to evaluate')
        parser.add_argument('-t','--test', nargs=1, help='Load test sentences from CSV file')
        parser.add_argument('-o','--out', nargs=1, help='Output test result to CSV file or -- for stdout')
        args = parser.parse_args()

        # Create a naive bayes instance
        naiveBayes = NaiveBayes()

        # Checkfor missing arguments
        if args.input is None and args.loadcache is None or args.out is None:
            print("Missing arguments")
            exit(1)

        # Load input csv
        if args.input is not None:
            print(">> Loading:", args.input[0])
            with open(args.input[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                naiveBayes.m_totalUtt = len(reader)
                for row in reader:
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
            
            # Compute probabilities
            naiveBayes.compute()

class NaiveBayes:
    def __init__(self):
        """Initialize naive bayes variables"""
        
        # Store counts
        self.m_totalUtt = 0
        self.m_categoryCounter= {}
        self.m_wordGivenCategoryCounter = {}
        self.m_wordsInCategoryCounter = {}

        # Store probabilities
        self.m_pWordGivenCategory = {}
        self.m_pCategory = {}

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
                if category in self.m_wordGivenCategoryCounter[word]:
                    self.m_pWordGivenCategory[word][category] = \
                            (BIAS +  self.m_wordGivenCategoryCounter[word][category]) / \
                            (self.m_wordsInCategoryCounter[category] + wordGivenCategoryCounter.size())


# Stat application
cli = CLI()
cli.read()
