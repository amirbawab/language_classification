import sklearn
import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import csv
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np
from threading import Thread

# Set target/output
categories = ['0','1','2','3','4']

# Set cores
cores = 8

# Load files
print(">> Loading data")
twenty_train = sklearn.datasets.load_files('/home/amirbawab/data/')

# Load new data
print(">> Loading test data")
docs_new = []
with open('/home/amirbawab/training_text.csv', newline='', encoding='utf-8') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         docs_new.append(row['Text'])

# Pipline function
def pipeline(itr,alpha):
    print(">> Creating pipeline with iteration={}, alpha={}".format(itr, alpha))
    text_clf = Pipeline([
        ('vect', CountVectorizer(stop_words=None,token_pattern='(?u)\\b\\w\\w*\\b')),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(
            loss='hinge', penalty='l1',alpha=alpha, random_state=42,max_iter=itr, tol=None, n_jobs=cores))])

    print(">> Predicting ...")
    text_clf.fit(twenty_train.data, twenty_train.target)
    predicted = text_clf.predict(docs_new)

    # Print to stdout
    c = 0
    filename = '/tmp/scikit-{}-{}.csv'.format(itr,alpha)
    print(">> Generating ouput:",filename)
    outputFile = open(filename,'w')
    outputFile.write('Id,Category\n')
    for doc, category in zip(docs_new, predicted):
        outputFile.write('{},{}\n'.format(c, twenty_train.target_names[category]))
        c += 1
    outputFile.close()

# New
threads = []
for itr in range(5,15,2):
    for lalpha in range(1,10,3):
        for ralpha in range(3,6):
            alpha = float('{}e-{}'.format(lalpha, ralpha))
            thread = Thread(target = pipeline, args = (itr,alpha,))
            threads.append(thread)
            thread.start()

# Join threads
for thread in threads:
    thread.join()

print(">> Done")
