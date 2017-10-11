import re
from math import sqrt
import nltk
import csv
import argparse

class KNN:
    self.languages = {}
    self.knn_results = {}
    self.y = {}
    self.test_vectors = {}

    def run_knn(self):
        parser = argparse.ArgumentParser(description='KNN algorithm')
        parser.add_argument('-t','--text', nargs=1, help='CSV text file')
        parser.add_argument('-l','--lang', nargs=1, help='CSV language file')
        parser.add_argument('-f','--test', nargs=1, help='CSV test file')
        args = parser.parse_args()
        load_language_list(args.lang[0])
        vectorize_training_data(args.text[0])
        vectorize_test(args.test[0])
        knn_calc()

    def load_language_list(self, yfile):
        with open(yfile, 'rb') as f:
            reader = csv.DictReader(csvfile)
            for row in reader:
                y.append(row['Category'])

    def vectorize_training_data(self, textfile):
        with open(textfile, 'rb') as f:
            reader = csv.DictReader(csvfile)
            for i in range(len(reader)):
                lang = self.y[i]
                row = reader[i]
                for word in nltk.word_tokenize(row['Text']):
                    if self.languages[lang].has_key(word):
                        self.languages[lang][word] += 1
                    else:
                        self.languages[lang][word] = 1

    def vectorize_test(self, f):
        with open(f, 'rb') as f:
            reader = csv.DictReader(csvfile)
            for i in range(len(reader)):
                self.test_vectors[i] = {}
                row = reader[i]
                for word in nltk.word_tokenize(row['Text']):
                    if self.test_vectors[i].has_key(word):
                        self.test_vectors[i][word] += 1
                    else:
                        self.test_vectors[i][word] = 1

    def knn_calc(self):
        for text in self.test_vectors.keys():
            self.knn_results[text] = {}
            for lang in self.languages.keys():
                distance = 0
                for word in self.test_vectors[text].keys():
                    if word in self.languages[lang].keys():
                        distance += (self.test_vectors[text][word] - self.languages[lang][word]) ** 2
                    else:
                        distance += (self.test_vectors[text][word] - 0) ** 2
                distance = sqrt(distance)
                self.knn_results[text][lang] = distance
            self.knn()

    def knn(self):
        closest_language = None
        closest_distance = None
        for lang in knn_results[test_row]:
            print(knn_results[test_row])
            if not closest_language or knn_results[test_row][lang] < closest_distance:
                closest_distance = knn_results[test_row][lang]
                closest_language = lang
        print('Predicted language: '+closest_language)

knn = KNN()
knn.read()
