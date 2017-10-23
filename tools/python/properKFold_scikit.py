import pandas as pd
import argparse

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

#path = '/Users/sunyambagga/Downloads/csv/kfold/'

import numpy as np
from sklearn.metrics import accuracy_score

algorithms = []
algorithms.append(('Multinomial Naive Bayes (scikit-learn implementation)', MultinomialNB()))
#algorithms.append(('Decision Trees', DecisionTreeClassifier()))
algorithms.append(('Logistic Regression', LogisticRegression()))
#algorithms.append(('Random Forests', RandomForestClassifier()))
#algorithms.append(('Multilayer Perceptron', MLPClassifier()))

results = []
def run():
    for (name, algo) in algorithms:
        print "Algorithm: ", name
        predictions = []
        for i in xrange(1,11):
            print "Running for k = ", str(i)
            train = pd.read_csv(args.path+'train/train'+str(i))
            train_clean = train.replace(np.nan, '', regex=True)
            
            vectorizer = CountVectorizer(decode_error='ignore', token_pattern='(?u)\\b\\w\\w*\\b')
            X_train = vectorizer.fit_transform(train['Text'].tolist())
            
            model = algo.fit(X_train, train['Category'].tolist())
            
            test = pd.read_csv(args.path+'test/test'+str(i))#, error_bad_lines=False)
            test.replace(np.nan, '', regex=True, inplace=True)
            
            X_test = vectorizer.transform(test['Text'])
            
            #     print X_train.shape
            #     print X_test.shape
            
            pred = model.predict(X_test)
            
            y_true = pd.read_csv(args.path+'valid/test'+str(i))['Category'].tolist()
            #     print len(pred), len(y_true)
            
            acc = accuracy_score(y_true, pred)
            print acc
            print "\n"
            predictions.append(acc)
        print "Done with ", name
        print "The mean accuracy is ", sum(predictions)/10.0
        print "\n\n###################################\n\n"
        results.append((name, predictions))

    print results
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()
    run()
