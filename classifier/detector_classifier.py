""""Classifier that replaces the current classifier with a new one when a change is detected in accuracy.
"""
from sklearn.metrics import accuracy_score
from sklearn import clone


class DetectorClassifier:
    def __init__(self, clf, detection_method):
        self.clf = clf
        self.detection_method = detection_method
        self.change_detected = 0

    def fit(self, X, y):
        self.clf.fit(X, y)
        return self

    def partial_fit(self, X, y):
        pre_y = self.clf.predict(X)
        if self.detection_method.set_input(accuracy_score(pre_y, y)):
            self.change_detected += 1
            self.clf = clone(self.clf)
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
