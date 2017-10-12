#run as python knn-library.py -f <space separated filename>

import os
import csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--knn", "-k", type=str, required=True)
args = parser.parse_args()

X = []
y = []
with open(args.file, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        X.append(row['Text'])
        y.append(row['Category'])

vec = CountVectorizer(input='content',analyzer='char',decode_error='ignore',stop_words=None,ngram_range=(1,1))
train_vectors = vec.fit_transform(X,y).toarray()

neigh = KNeighborsClassifier(n_neighbors=int(args.knn[0]))
neigh.fit(train_vectors, y)
y_pred = neigh.predict(train_vectors)
print(metrics.accuracy_score(y, y_pred))
