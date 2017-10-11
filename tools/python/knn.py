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

    def knn(self):
        for test_row in self.test_vectors.keys():
            closest_language = None
            closest_distance = None
            for lang in self.knn_results[test_row]:
                print(self.knn_results[test_row])
                if not closest_language or self.knn_results[test_row][lang] < closest_distance:
                    closest_distance = self.knn_results[test_row][lang]
                    closest_language = lang
            print('Predicted language: '+closest_language)


    def knn_calc(self):
        for test_row in self.test_vectors.keys():
            self.knn_results[test_row] = {}
            for lang in self.languages.keys():
                distance = 0
                for word in self.test_vectors[test_row].keys():
                    if word in self.languages[lang].keys():
                        distance += (self.test_vectors[test_row][word] - self.languages[lang][word]) ** 2
                    else:
                        distance += (self.test_vectors[test_row][word] - 0) ** 2
                distance = sqrt(distance)
                self.knn_results[test_row][lang] = distance
        self.knn()

    def run_knn(self):
        parser = argparse.ArgumentParser(description='KNN algorithm')
        parser.add_argument('-f','--text', nargs=1, help='CSV text and language file')
        # parser.add_argument('-l','--lang', nargs=1, help='CSV language file')
        parser.add_argument('-t','--test', nargs=1, help='CSV test file')
        args = parser.parse_args()
        # load_language_list(args.lang[0])
        self.vectorize_training_data(args.text[0])
        self.vectorize_test(args.test[0])
        self.knn_calc()



knn = KNN()
knn.run_knn()
