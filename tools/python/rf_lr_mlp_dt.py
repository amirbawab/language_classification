import csv
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold, cross_val_score

X = []
Y = []
trainX = []
testX = []
trainY = []
testY = []

def read_data():
    with open(args.path, 'rb') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            X.append(row[1])
            Y.append(row[0])
    print "\n\n" + str(len(X)) + " lines of data.\n"

# Vectorisation
def vectorise():
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(decode_error='ignore', token_pattern='(?u)\\b\\w\\w*\\b')
    X_floats = vectorizer.fit_transform(X)
    print "\nVectorised: ", X_floats.shape
    return X_floats

def run(X_floats):
    kfold = KFold(n_splits=10, random_state=5)
    print "\n\nRunning algorithms now....\n\nNOTE: RandomForests and Neural Nets take about 20 mins to complete 10-folds.\n\n"
    algorithms = []
    algorithms.append(('Multinomial Naive Bayes (scikit-learn implementation)', MultinomialNB()))
    algorithms.append(('Decision Trees', DecisionTreeClassifier()))
#    algorithms.append(('Logistic Regression', LogisticRegression()))
#    algorithms.append(('Random Forests', RandomForestClassifier()))
#    algorithms.append(('Multilayer Perceptron', MLPClassifier()))


    results = []
    algo_names = []
    for name, algo in algorithms:
        print "Running ", name
        cv_results = cross_val_score(algo, X_floats, Y, cv=kfold, scoring='accuracy')
        print "Mean accuracy for ", name
        print cv_results.mean()
        print "\n\n"
        algo_names.append(name)
        results.append(cv_results)

    if args.plot:
        import matplotlib.pyplot as plt

        # Adding enhanced Naive Bayes results:
        new_results = results.append([0.8970, 0.8974, 0.8969, 0.8961, 0.8990, 0.8966, 0.8976, 0.8996, 0.8960, 0.8950])
        algo_names.append('Naive Bayes (from scratch)')
#        print new_results
#        print algo_names
        for name, res in zip(algo_names, results):
            l1 = plt.plot(range(1,11), res, label=name, linewidth=2.0, linestyle='-')

        l1[-1].set_color('b')
        plt.xlabel('K=10 folds', fontsize=12)
        plt.ylabel('Accuracy', fontsize=12)
        # plt.legend()
        plt.legend(bbox_to_anchor=(0, 1), loc='lower left')

        plt.show()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-plot", action='store_true', help="Plot the graph")
    ap.add_argument("path")
    args = ap.parse_args()
    path = args.path
    read_data()
    X_floats = vectorise()
    run(X_floats)


