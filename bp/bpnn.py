__author__ = 'AaronSun'
# Back-Propagation Neural Networks

import csv
import json
import math
import random
import string
from numpy import genfromtxt
from prepareData import PrepareData

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)

        #read from file
        self.readWeight(self.wi, self.ni, self.nh, 1)
        self.readWeight(self.wo, self.nh, self.no, 2)

        #print(self.wi)

        #if read failed, then generate from random
        # set them to random values
        #change it to read from weights.csv
        #for i in range(self.ni):
            #for j in range(self.nh):
             #   self.wi[i][j] = rand(-0.2, 0.2)
        #for j in range(self.nh):
         #   for k in range(self.no):
          #      self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]
        self.writeWeight(self.wo, self.nh, self.no, 2)

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change
        self.writeWeight(self.wi, self.ni, self.nh, 1)

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
        for p in patterns:
            #print(p[0], '->', self.update(p[0]))
            print(self.label(self.update(p[0])))

            # output part
            #
            #
            #
            #

    #output the MBTI lables
    #make it a string list, not a array
    def label(self, result):
        print(result)
        output = []
        if result[0] < 0.5 :
                output=output+["E"]
        else :
                output=output+["I"]
        if result[1] < 0.5 :
                output=output+["N"]
        else :
                output=output+["S"]
        if result[2] < 0.5 :
                output=output+["T"]
        else :
                output=output+["F"]
        if result[3] < 0.5 :
                output=output+["J"]
        else :
                output=output+["P"]
        return output


    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def readWeight(self, w, x, y, index): #index is the location of the weights in file

        if index == 1:
            file = open("InputLayer.csv", "r") # the weights
            my_data = genfromtxt('InputLayer.csv', delimiter=',')
            #print(my_data[index].size)
            #print(x*y)
        else:
            file = open("HiddenLayer.csv", "r") # the weights
            my_data = genfromtxt('HiddenLayer.csv', delimiter=',')

        if my_data[0].size == x*y:
            for i in range(x):
                for j in range(y):
                    count=0
                    w[i][j] = my_data[1][count]
                    count=count+1
        else:
            for i in range(x):
                for j in range(y):
                    w[i][j] = rand(-0.2, 0.2)

    def writeWeight(self, weight, x, y, index):
        if index == 1:
            path = 'InputLayer.csv'
        else:
            path = 'HiddenLayer.csv'
        weight_list=[]
        with open(path, 'r') as b:
            original = csv.reader(b)
            weight_list.extend(original)
            #print('weight', weight_list)

        #update header row
        header = []
        for i in range(x*y):
            header.append('1')
        #header_to_write = {0:header}

        serial_data = []
        for i in range(x):
            for j in range(y):
                serial_data.append(weight[i][j])
        #if index == 1:
            #print(serial_data)

        data_to_write={1:serial_data, 0:header}
            #print('serial', serial_data)

            #update header row
            # #header=[]
            #for i in range(x*y):
            #    header.append('1')
            #header_to_write = {0:header}


        with open(path, 'w') as b:
            writer = csv.writer(b)
            for line, row in enumerate(weight_list):
                data = data_to_write.get(line, row)
                writer.writerow(data)
                #print('write', data)




    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        count = 0
        while True :
            count = count + 1
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
                print('error %-.5f' % error)
            if error < 0.1 or count == iterations:
                break
            count = count + 1

def demo():
    # assign patterns here.
    #pat = [
     #   [[0.7,0.4,1,1], [0,1,1,1]],
      #  [[0.9,0.6,1,0.9], [1,1,0,1]],
       # [[0.7,1,1,0.5], [0,1,1,0]],
        #[[1,0.9,0.1,0.2], [0,1,1,1]]
    #]
    pat=[[],[]]
    #import data from raw data
    x=PrepareData()
    x.runSample()
    pat = x.sample
    print(pat[0][0])
    #print(x.sample[1][1])
    #print(len(pat[1]))
    # create a network with two input, two hidden, and one output nodes
    n = NN(len(pat[0][0]), 4, 4)
    # train it with some patterns
    n.train(pat)


    x.runTest()
    test = x.target
    # test it
    n.test(test)




if __name__ == '__main__':
    demo()

#implementations:
#1. work out the implementation symble for MBTI
#2. round the final data, to get absolutly 0 or 1.
#3. a read csv file function.
#4. manipulate the file into "pat" format.
#5. save the weights for re-use

