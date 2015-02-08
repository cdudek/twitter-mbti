__author__ = 'AaronSun'

from sklearn import preprocessing
class PrepareData:
    def __init__(self):
        self.sample = []
        self.length

from numpy import genfromtxt
import numpy as np


file = open("./bp/Raw_Data.csv", "r") # the raw data
my_data = genfromtxt('./bp/Raw_Data.csv', delimiter=',')
#print(my_data[1][1])

#sector for scaling raw data and put into sample[] in the format:
#[[sample inputs],[outputs]]

X_train = np.array(my_data)
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)

# above codes are not tested. need Scipy library, but fail to install. shit.

#sample=X_train_minmax
sample = []

for p in X_train_minmax:
    for i in range(0, p.size):
        sample[0] = sample[0]+p[i]
    for j in range (0, 3):
        sample[1] = sample[1]+p[j]
print (sample)
# I am seriously wrong here, I suppose... need help.
