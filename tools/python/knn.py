import re
from math import sqrt
import nltk
import csv
import argparse

class KNN:

    def __init__(self):
        self.languages = {}
        self.knn_results = {}
        self.test_vectors = {}

    def vectorize_training_data(self, textfile):
        with open(textfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lang = row['Category']
                if self.languages.get(lang) is None:
                    self.languages[lang] = {}
                for word in nltk.word_tokenize(row['Text']):
                    if self.languages[lang].has_key(word):
                        self.languages[lang][word] += 1
                    else:
                        self.languages[lang][word] = 1

    def vectorize_test(self, testfile):
        with open(testfile, 'rb') as csvfile:
            i = 0
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.test_vectors[i] = {}
                for word in nltk.word_tokenize(row['Text']):
                    if self.test_vectors[i].has_key(word):
                        self.test_vectors[i][word] += 1
                    else:
                        self.test_vectors[i][word] = 1
                i += 1

    def predict(self, outfile):
        predictions = {}
        f = open(outfile, 'w')
        f.write('Id,Category\n')
        for i in range(len(self.knn_results)):
            predictions[i] = {}
            for lang,v in self.knn_results[i].iteritems():
                if lang in predictions[i]:
                    predictions[i][lang] += 1
                else:
                    predictions[i][lang] = 1
            language_predicted = sorted(predictions[i].iteritems(), key=lambda (k,v): (v,k), reverse=True)[0][0]
            f.write(str(i)+','+str(language_predicted)+'\n')
        f.close()

    def knn_calc(self, k, outfile):
        for test_row in self.test_vectors.keys():
            self.knn_results[test_row] = {}
            neighbours = {}
            for lang in self.languages.keys():
                distance = 0
                for word in self.test_vectors[test_row].keys():
                    if word in self.languages[lang].keys():
                        distance += (self.test_vectors[test_row][word] - self.languages[lang][word]) ** 2
                    else:
                        distance += (self.test_vectors[test_row][word] - 0) ** 2
                neighbours[lang] = sqrt(distance)
            neighbours = sorted(neighbours.iteritems(), key=lambda (k,v): (v,k))
            for i in range(int(k)):
                self.knn_results[test_row][neighbours[i][0]] = neighbours[i][1]
        self.predict(outfile)

    def run_knn(self):
        parser = argparse.ArgumentParser(description='KNN algorithm')
        parser.add_argument('-f','--text', nargs=1, help='CSV text and language file')
        parser.add_argument('-k','--knn', nargs=1, help='Number of nearest neighbours')
        parser.add_argument('-t','--test', nargs=1, help='CSV test file')
        parser.add_argument('-o','--out', nargs=1, help='output CSV file')
        args = parser.parse_args()
        self.vectorize_training_data(args.text[0])
        self.vectorize_test(args.test[0])
        self.knn_calc(args.knn[0], args.out[0])


knn = KNN()
knn.run_knn()
