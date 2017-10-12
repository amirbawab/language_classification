
import csv

X = []
Y = []
trainX = []
testX = []
trainY = []
testY = []

'''
   Splits training data into train/test with the first 240,000 samples in train and the rest ~30,000 in test.
'''
def splitTrainTest():
    path = '/Users/sunyambagga/Desktop/Applied ML 551/Project 2/result.csv'
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            X.append(row[1])
            Y.append(row[0])

    for x in X[:240000]:
        trainX.append(x)
        
        for x in X[240000:]:
            testX.append(x)
        
        for y in Y[:240000]:
            trainY.append(y)
        
        for y in Y[240000:]:
            testY.append(y)

splitTrainTest()
print "Train X: ", len(trainX)
print "Train Y: ", len(trainY)
print "Test X: ", len(testX)
print "Test Y: ", len(testY)

'''
    Vectorising the dataset:
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score

vectorizer = CountVectorizer(decode_error='ignore', token_pattern='(?u)\\b\\w\\w*\\b')

X_train = vectorizer.fit_transform(trainX)

X_test = vectorizer.transform(testX)

print "\n\nVectoriser Shape:\n"
print X_train.shape
print X_test.shape

'''
    Machine Learning algorithms:
    1. Doing it the proper train/test way.
'''
print "Logistic Regression training...."
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression().fit(X_train, trainY)
pred_lr = lr.predict(X_test)
print "\nLogistic Regression: ", accuracy_score(testY, pred_lr)

print "Neural Network training...."
from sklearn.neural_network import MLPClassifier
# nn = MLPClassifier(solver='sgd', learning_rate='adaptive').fit(X_train, trainY) # Gives 85.97
nn = MLPClassifier().fit(X_train, trainY) # Gives 86.25
pred_nn = nn.predict(X_test)
print "\nNeural Net: ", accuracy_score(testY, pred_nn)

print "Random Forest training...."
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier().fit(X_train, trainY)
pred_rf = rf.predict(X_test)
print "\nRandom Forest: ", accuracy_score(testY, pred_rf)
