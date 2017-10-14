import re
from math import sqrt
import nltk
import csv
import argparse
from collections import OrderedDict


class KNN:

    def __init__(self):
        self.train_vectors = {}
        self.y = {}
        self.knn_results = {}
        self.test_vectors = OrderedDict({})
        self.log_file = None

    def write_to_log(self,text):
        with open(self.log_file,'a') as logger:
            logger.write(text+'\n')

    def vectorize_training_data(self, textfile):
        self.write_to_log("-------------Vectorizing training data--------------")
        word_count_in_languages = {}
        with open(textfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_id = row['Id']
                if int(row_id)%10000 == 0: self.write_to_log("Vectorizing training row: "+row_id)
                self.y[row_id] = row['Category']
                if self.train_vectors.get(row_id) is None:
                    self.train_vectors[row_id] = {}
                for word in nltk.word_tokenize(row['Text']):
                    try:
                        self.train_vectors[row_id][word] += 1
                    except KeyError:
                        self.train_vectors[row_id][word] = 1
                for word, freq in self.train_vectors[row_id].iteritems():
                    self.train_vectors[row_id][word] = float(self.train_vectors[row_id][word]) / float(sum(self.train_vectors[row_id].values()))
        self.write_to_log("-------------Completed vectorizing training data--------------")

    def vectorize_test(self, testfile):
        self.write_to_log("-------------Vectorizing test data--------------")
        with open(testfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_id = row['Id']
                if int(row_id)%1000 == 0: self.write_to_log("Vectorizing test row: "+row_id)
                self.test_vectors[row_id] = {}
                for word in nltk.word_tokenize(row['Text']):
                    try:
                        self.test_vectors[row_id][word] += 1
                    except KeyError:
                        self.test_vectors[row_id][word] = 1
                for word in nltk.word_tokenize(row['Text']):
                    self.test_vectors[row_id][word] = float(self.test_vectors[row_id][word]) / float(sum(self.test_vectors[row_id].values()))
        self.write_to_log("-------------Completed vectorizing test data--------------")

    def knn_calc(self, k, outfile):
        self.write_to_log("-------------Calculating nearest neighbours--------------")
        f = open(outfile, 'w')
        f.write('Id,Category\n')
        predictions = {}
        for test_row in self.test_vectors.keys():
            self.knn_results[test_row] = {}
            neighbours = {}
            if int(test_row)%10000 == 0: self.write_to_log("Calculating distances for row_id: "+test_row)
            for row_id in self.train_vectors.keys():
                neighbours[row_id] = sqrt(sum({word: (self.test_vectors[test_row][word] - self.train_vectors[row_id].get(word,0))**2 for word in self.test_vectors[test_row].keys()}.values()))
            neighbours = sorted(neighbours.iteritems(), key=lambda (k,v): (v,k))
            if int(test_row)%10000 == 0: self.write_to_log("Predicting language for test row_id: "+test_row)
            predictions[test_row] = {}
            for i in range(int(k)):
                row_id = neighbours[i][0]
                lang = self.y[row_id]
                try:
                    predictions[test_row][lang] += 1
                except KeyError:
                    predictions[test_row][lang] = 1
            language_predicted = sorted(predictions[test_row].iteritems(), key=lambda (k,v): (v,k), reverse=True)[0][0]
            f.write(str(test_row)+','+str(language_predicted)+'\n')
        f.close()

    def run_knn(self):
        parser = argparse.ArgumentParser(description='KNN algorithm')
        parser.add_argument('-f','--text', nargs=1, help='CSV text and language file',required=True)
        parser.add_argument('-k','--knn', nargs=1, help='Number of nearest neighbours',required=True)
        parser.add_argument('-t','--test', nargs=1, help='CSV test file',required=True)
        parser.add_argument('-o','--out', nargs=1, help='output CSV file',required=True)
        parser.add_argument('-l','--logfile', nargs=1, help='log file',required=True)
        args = parser.parse_args()
        self.log_file = args.logfile[0]
        self.vectorize_training_data(args.text[0])
        self.vectorize_test(args.test[0])
        self.knn_calc(args.knn[0], args.out[0])

knn = KNN()
knn.run_knn()
