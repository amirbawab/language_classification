path = '/Users/sunyambagga/Desktop/Applied ML 551/Project 2/100k_result.csv'

import pandas as pd
df = pd.read_csv(path)
df.drop('Id', axis=1, inplace=True)

Y_mil = []
for i in df['Category']:
    Y_mil.append(i)

X_mil = []
for i in df['Text']:
    X_mil.append(i)

print "X: ", len(X_mil)
print "Y: ", len(Y_mil)

# Training on 1 million:
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score

vectorizer = CountVectorizer(decode_error='ignore', token_pattern='(?u)\\b\\w\\w*\\b')
X_train = vectorizer.fit_transform(X_mil)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(verbose=1).fit(X_train, Y_mil) # takes 33.5 mins to train.

# Testing on 270k:
path = '/Users/sunyambagga/Desktop/result.csv'
import csv

X = []
Y = []
with open(path, 'rb') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        X.append(row[1])
        Y.append(row[0])

Y_int = [int(x) for x in Y]

X_test = vectorizer.transform(X)
print X_test.shape

pred_rf_mil = rf.predict(X_test)
print "Random Forest: ", accuracy_score(Y_int, pred_rf_mil)
