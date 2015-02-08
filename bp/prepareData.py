__author__ = 'AaronSun'

from sklearn import preprocessing
from numpy import genfromtxt
import numpy as np

# ins: give the exact path for all the files.

class PrepareData:
    def __init__(self):
        self.sample = []
        self.target = []
        self.file = open("/Users/AaronSun/Downloads/twitter-mbti-master/samples.csv", "r") # the raw data
        self.my_data = genfromtxt('/Users/AaronSun/Downloads/twitter-mbti-master/samples.csv', delimiter=',')
        self.Testfile = open("", "r") # the raw data
        self.my_Testdata = genfromtxt('', delimiter=',')

    def runSample(self):
        X_train = np.array(self.my_data)
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train_minmax = min_max_scaler.fit_transform(X_train)

        # above codes are not tested. need Scipy library, but fail to install. shit.

        #sample=X_train_minmax
        #target = [[],[]]
        print(X_train_minmax)
        processed_samples = []
        for p in X_train_minmax:
            count = 0
            next_sample = []
            next_sample.append(p[4:])
            next_sample.append(p[0:4])
            processed_samples.append(next_sample)
            count = count+1

        self.sample = processed_samples
        print('sample:...', self.sample[0][1])

    def runTest(self):
        X_test = np.array(self.my_Testdata)
        min_max_scaler = preprocessing.MinMaxScaler()
        X_test_minmax = min_max_scaler.fit_transform(X_test)

        processed_tests = []
        for p in X_test_minmax:
            count = 0
            next_test = []
            next_test.append(p[:])
            next_test.append([1,1,1,1])
            processed_tests.append(next_test)
            count = count+1
        self.target = processed_tests











