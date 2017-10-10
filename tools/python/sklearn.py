import sklearn
import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

print("Loading data ...")
categories = ['0','1','2','3','4']
twenty_train = sklearn.datasets.load_files('/tmp/ml/data/')
count_vect = CountVectorizer(stop_words=None,token_pattern='(?u)\\b\\w\\w*\\b')
X_train_counts = count_vect.fit_transform(twenty_train.data)
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
docs_new = [
        'd e s m e n s o n g e s p a s v r a i m e n t n o n c e s t j u s t e q u e c e s t l e s',
        'j e t z t w i r d s a b e r w i r k l i c h e r d i g h e u t e s t e l l i c h e u c h d i e']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
