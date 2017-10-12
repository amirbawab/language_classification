import re
from math import sqrt
import nltk
import csv
import argparse

class KNN:

    def __init__(self):
        self.train_vectors = {}
        self.y = {}
        self.knn_results = {}
        self.test_vectors = {}

    def vectorize_training_data(self, textfile):
        word_count_in_languages = {}
        with open(textfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_id = row['Id']
                self.y[row_id] = row['Category']
                if self.train_vectors.get(row_id) is None:
                    self.train_vectors[row_id] = {}
                for word in nltk.word_tokenize(row['Text']):
                    if self.train_vectors[row_id].has_key(word):
                        self.train_vectors[row_id][word] += 1
                    else:
                        self.train_vectors[row_id][word] = 1
                for word, freq in self.train_vectors[row_id].iteritems():
                    self.train_vectors[row_id][word] = float(self.train_vectors[row_id][word]) / float(sum(self.train_vectors[row_id].values()))

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
                for word in nltk.word_tokenize(row['Text']):
                    self.test_vectors[i][word] = float(self.test_vectors[i][word]) / float(sum(self.test_vectors[i].values()))
                i += 1

    def predict(self, outfile):
        predictions = {}
        f = open(outfile, 'w')
        f.write('Id,Category\n')
        for i in range(len(self.knn_results)):
            predictions[i] = {}
            for row_id,v in self.knn_results[i].iteritems():
                lang = self.y[row_id]
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
            for row_id in self.train_vectors.keys():
                distance = 0
                for word in self.test_vectors[test_row].keys():
                    if word in self.train_vectors[row_id].keys():
                        distance += (self.test_vectors[test_row][word] - self.train_vectors[row_id][word]) ** 2
                    else:
                        distance += (self.test_vectors[test_row][word] - 0) ** 2
                neighbours[row_id] = sqrt(distance)
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
