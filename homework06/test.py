import csv
from normalize import normalize
from bayes import NaiveBayesClassifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == '__main__':

    with open('SMSSpamCollection') as f:
         data = list(csv.reader(f, delimiter="\t"))

    model = NaiveBayesClassifier()

    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
     
    X = [normalize(x) for x in X]

    model.fit(X_train, y_train)
    print('score =', model.score(X_test, y_test))

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
