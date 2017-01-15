"""Batch-Incremental Ensemble Classifier
Collect w(decided by first fit data) training examples, then build a batch model with these examples and repeat.
"""
import numpy as np
from sklearn import clone


class BatchClassifier:
    def __init__(self, clf, clf_number=5):
        self.counter = 0
        self.clf = clf
        self.clf_number = clf_number
        self.clf_list = []
        self.X_batch = []
        self.Y_batch = []

    def fit(self, X, y):
        clf = clone(self.clf)
        clf.fit(X, y)
        self.clf_list.append(clf)
        self.X_batch = np.zeros(X.shape)
        self.Y_batch = np.zeros(y.shape)
        return self

    def partial_fit(self, X, y):
        try:
            # Add to batch
            self.X_batch[self.counter] = X
            self.Y_batch[self.counter] = y
            self.counter += 1
        except IndexError:
            clf = clone(self.clf)
            clf.fit(self.X_batch[:self.counter], self.Y_batch[:self.counter])
            if len(self.clf_list) == self.clf_number:
                self.clf_list.pop(0)
            self.clf_list.append(clf)
            self.counter = 0
        return self

    def predict(self, x):
        sum_pre = np.zeros(x.shape[0])
        for clf in self.clf_list:
            # Sum the predict
            sum_pre = np.add(sum_pre, clf.predict(x))
        sum_pre /= len(self.clf_list)
        result = (sum_pre >= 0.5).astype(int)
        return result
