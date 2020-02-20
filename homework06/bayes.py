from math import log
from collections import Counter, defaultdict
from normalize import normalize


class NaiveBayesClassifier:

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.classes = defaultdict(lambda: defaultdict(int))
        self.words = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def fit(self, X, y):
        all_words = []
        self.classes_counter = dict(Counter(y))
        for title, class_ in zip(X, y):
            word_list = normalize(title)
            for word in word_list:
                all_words.append(word)
                self.classes[class_]['words_in_class'] += 1
                self.words[word][class_]['appearances'] += 1

        for class_ in self.classes:
            self.classes[class_]['prior'] = self.classes_counter[class_] / \
                len(y)
        words_counter = dict(Counter(all_words))
        vector_size = len(Counter(all_words))

        for word in words_counter:
            for class_ in self.classes:
                self.words[word][class_]['probability'] = (
                    self.words[word][class_].get('appearances', 0) +
                    self.alpha) / \
                    (self.classes[class_]['words_in_class'] +
                     vector_size * self.alpha)

    def predict(self, X):
        classification = []
        for title in X:
            probabilities = []  # probabilities of word relation to a class
            word_list = normalize(title)
            for class_ in self.classes:
                title_prob = log(self.classes[class_]['prior'])
                for word in word_list:
                    if self.words[word][class_]:
                        title_prob += log(self.words[word][class_]
                                          ['probability']
                                          )
                probabilities.append((class_, title_prob))
            classification.append(max(probabilities, key=lambda x: x[1])[0])
        return classification

    def score(self, X_test, y_test):
        count = 0
        for record, label in zip(self.predict(X_test), y_test):
            if record[0] == label:
                count += 1
        return count / len(y_test)
