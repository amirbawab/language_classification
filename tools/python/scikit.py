import sklearn
import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import csv
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np

# Set target/output
categories = ['0','1','2','3','4']

print("Loading data ...")
twenty_train = sklearn.datasets.load_files('/tmp/ml/data/')

# Allow words with one characters
count_vect = CountVectorizer(stop_words=None,token_pattern='(?u)\\b\\w\\w*\\b')

# Train
X_train_counts = count_vect.fit_transform(twenty_train.data)
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)

#X_train_tf = tf_transformer.transform(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# Load new data
docs_new = []
with open('/tmp/test_set_x.csv', newline='', encoding='utf-8') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         docs_new.append(row['Text'])

# Predict
#X_new_counts = count_vect.transform(docs_new)
#X_new_tfidf = tfidf_transformer.transform(X_new_counts)
#predicted = clf.predict(X_new_tfidf)

# New
text_clf = Pipeline([('vect', count_vect),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None))])
text_clf.fit(twenty_train.data, twenty_train.target)
predicted = text_clf.predict(docs_new)

# Print to stdout
#c = 0
#print('Id,Category')
#for doc, category in zip(docs_new, predicted):
#    print('{},{}'.format(c, twenty_train.target_names[category]))
#    c += 1
