import os
import csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--knn", "-k", type=str, required=True)
parser.add_argument('-t','--test', nargs=1, help='CSV test file', required=True)
parser.add_argument('-o','--out', nargs=1, help='output CSV file', required=True)
args = parser.parse_args()

X = []
y = []
X_test = []
with open(args.file, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        X.append(row['Text'])
        y.append(row['Category'])

with open(args.test[0], 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        X_test.append(row['Text'])

vec = CountVectorizer(input='content',analyzer='char',decode_error='ignore',stop_words=None,ngram_range=(1,1))
train_vectors = vec.fit_transform(X,y).toarray()
test_vectors = vec.transform(X_test).toarray()

neigh = KNeighborsClassifier(n_neighbors=int(args.knn[0]))
neigh.fit(train_vectors, y)
y_pred = neigh.predict(test_vectors)

f = open(args.out[0],'w')
f.write('Id,Category\n')
i = 0
for i in range(len(y_pred)):
    f.write(str(i)+','+str(y_pred[i])+'\n')
f.close()
