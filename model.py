# coding: utf-8

from const import *
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.externals import joblib
import csv
import time
import numpy as np
import sys
import os

def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
    # model = LinearSVC(C=1)
    # model = RandomForestClassifier(n_estimators = 100)
    # model = LogisticRegression(C = 1,penalty = 'l2', tol = 0.001, max_iter = 20000)
    # model.fit(X_train, y_train)
    model = SVR()
    model.fit(X, y)
    y_pred = model.predict(X_test)
    error = 0
    for i in range(len(y_test)):
        error = error + abs(y_test[i] - y_pred[i])
    error = error/len(y_test)
    return model

if __name__ == '__main__':
    train_data = np.array(pd.read_csv(MODEL_TRAIN_SET, index_col=0).dropna())
    test_data = np.array(pd.read_csv(MODEL_TEST_X_SET))
    test_data = pd.read_csv(MODEL_TEST_X_SET)
    X = train_data[:, :-1]
    y = train_data[:, -1]
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    X_test = scaler.transform(test_data)

    model = train(X, y)
    y_pred = model.predict(X_test)
    real_playtimes = pd.read_csv(MODEL_TEST_REAL_SET)
    print real_playtimes.isnull().sum().sum()
    real_playtimes = np.array(pd.read_csv(MODEL_TEST_REAL_SET))
    days = len(real_playtimes[0])
    y_pred = np.array([[x]*days for x in y_pred])

    sigma = ((y_pred-real_playtimes)/real_playtimes)**2
    sigma = np.sqrt(sigma.sum(axis = 1)/days)
    print sigma
    phi = np.sqrt(real_playtimes.sum(axis = 1))
    F = (sigma * phi).sum()
    Best = phi.sum()
    print F
    print Best
    print F/Best
