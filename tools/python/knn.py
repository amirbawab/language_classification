import re
from math import sqrt
import nltk
import csv
import argparse
import time
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import threading
import os

class KNN:

    def __init__(self):
        self.train_vectors = {}
        self.y = []
        self.id = []
        self.knn_results = {}
        self.categories = {}
        self.test_vectors = OrderedDict({})
        self.log_file = None

    def write_to_log(self,text):
        with open(self.log_file,'a') as logger:
            logger.write(text+'\n')

    def vectorize_training_and_test_data(self, trainfile,testfile):
        self.write_to_log("-------------Vectorizing training and test data--------------")
        X = []
        X_test = []
        with open(trainfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                X.append(row['Text'])
                self.y.append(row['Category'])

        with open(testfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                X_test.append(row['Text'])
                self.id.append(row['Id'])
        vec = CountVectorizer(input='content',analyzer='char',decode_error='ignore',stop_words=None,ngram_range=(1,1))
        self.train_vectors = vec.fit_transform(X,self.y).toarray()
        self.test_vectors = vec.transform(X_test).toarray()

    def predict_knn(self,k,outfile,start,end):
        self.write_to_log("-------------Calculating nearest neighbours--------------")
        f = open(outfile, 'w')
        f.write('Id,Category\n')
        predictions = {}
        neighbours = {}
        for test_row in range(start,end):
            if int(test_row)%1000 == 0: self.write_to_log("Calculating distances and prediction for row_id: "+str(test_row))
            neighbours[test_row] = numpy.sqrt(numpy.sum((self.train_vectors - self.test_vectors[test_row])**2,axis=1)).argsort()[:int(k)]
            predictions[test_row] = {}
            for i in range(int(k)):
                row_id = neighbours[test_row][i]
                lang = self.y[row_id]
                try:
                    predictions[test_row][lang] += 1
                except KeyError:
                    predictions[test_row][lang] = 1
            language_predicted = sorted(predictions[test_row].iteritems(), key=lambda (ke,v): (v,ke), reverse=True)[0][0]
            f.write(str(self.id[test_row])+','+str(language_predicted)+'\n')
        f.close()

    def vectorize_training_data(self, textfile):
        self.write_to_log("-------------Vectorizing training data--------------")
        word_count_in_languages = {}
        with open(textfile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_id = row['Id']
                if int(row_id)%10000 == 0: self.write_to_log("Vectorizing training row: "+row_id)
                self.categories[row_id] = row['Category']
                if self.train_vectors.get(row_id) is None: self.train_vectors[row_id] = {}
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
            neighbours = sorted(neighbours.iteritems(), key=lambda (ke,v): (v,ke))[0:k]
            if int(test_row)%10000 == 0: self.write_to_log("Predicting language for test row_id: "+test_row)
            predictions[test_row] = {}
            for i in range(int(k)):
                row_id = neighbours[i][0]
                lang = self.categories[row_id]
                try:
                    predictions[test_row][lang] += 1
                except KeyError:
                    predictions[test_row][lang] = 1
            language_predicted = sorted(predictions[test_row].iteritems(), key=lambda (k,v): (v,k), reverse=True)[0][0]
            f.write(str(test_row)+','+str(language_predicted)+'\n')
        f.close()


    def classify_text(self, textfile, testfile, k_count, outfile, vectorize, start, end, thread_id=None):
        if vectorize is None:
            self.vectorize_training_data(textfile)
            self.vectorize_test(testfile)
            self.knn_calc(k_count, outfile)
        else:
            dir_name = os.path.dirname(outfile)
            base = os.path.basename(outfile)
            f = os.path.splitext(base)
            outfile = os.path.join(dir_name,f[0]+str(thread_id)+f[1])
            self.predict_knn(k_count,outfile,start,end)


    def run_knn(self):
        parser = argparse.ArgumentParser(description='KNN algorithm')
        parser.add_argument('-f','--text', nargs=1, help='CSV text and language file',required=True)
        parser.add_argument('-k','--knn', nargs=1, help='Number of nearest neighbours',required=True)
        parser.add_argument('-t','--test', nargs=1, help='CSV test file',required=True)
        parser.add_argument('-o','--out', nargs=1, help='output CSV file',required=True)
        parser.add_argument('-l','--logfile', nargs=1, help='log file',required=True)
        parser.add_argument('-thread', action='store_true', help='Perform threading for knn')
        parser.add_argument('-c','--vectorize', action='store_true', help='pass a value to use CountVectorizer to vectorize data else use term frequency')
        args = parser.parse_args()
        self.log_file = args.logfile[0]
        if args.vectorize:
            self.vectorize_training_and_test_data(args.text[0], args.test[0])
        threads = []
        st = 0
        en = 15000
        if args.thread:
            for i in range(8):
                t = threading.Thread(target=self.classify_text, args = (args.text[0],args.test[0],args.knn[0],args.out[0],args.vectorize,st,en,i))#kwargs={'textfile':args.text[0], 'testfile':args.test[0], 'k_count':args.knn[0], 'outfile':args.out[0], 'vectorize':args.vectorize})
                st+=15000
                if i == 6:
                    en = len(self.test_vectors)
                else:
                    en+=15000
                threads.append(t)
                t.start()


knn = KNN()
knn.run_knn()
