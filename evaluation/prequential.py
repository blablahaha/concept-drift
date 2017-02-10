from time import clock

import numpy as np


def prequential(X, y, clf, n_train=1):
    """Prequential Evaluation: instances are first used to test, and then to train
    :return the label predictions for each test instance, and the associated running time
    """
    row_num = y.shape[0]
    # Split an init batch
    X_init = X[0:n_train]
    y_init = y[0:n_train]

    # Used for training and evaluation
    X_train = X[n_train:]
    y_train = y[n_train:]

    y_pre = np.zeros(row_num - n_train)
    time = np.zeros(row_num - n_train)

    clf.fit(X_init, y_init)

    for i in range(0, row_num - n_train):
        start_time = clock()
        y_pre[i] = clf.predict(X_train[i, :].reshape(1, -1))
        clf.partial_fit(X_train[i, :].reshape(1, -1), y_train[i].reshape(1, -1).ravel())
        time[i] = clock() - start_time

    return y_pre, time
