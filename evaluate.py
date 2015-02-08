import json
from models.User import User
from controller.UserController import UserController

import sample_analysis

def predict(data):
    type = [0, 0, 0, 0]
    return type

def decodeType(type):
    decoded = ""
    if(type[0] == 0):
        decoded += "E"
    else:
        decoded += "I"
    if(type[1] == 0):
        decoded += "N"
    else:
        decoded += "S"
    if(type[2] == 0):
        decoded += "T"
    else:
        decoded += "F"
    if(type[3] == 0):
        decoded += "J"
    else:
        decoded += "P"
    return decoded

def main(name):
    uc = UserController()
    followers = uc.getFollowers(name)

    result = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    type = [i, j, k, l]
                    result[decodeType(type)] = []

    for name in followers:
        print "next {}".format(name)
        user = User(name, "unknown")
        data = sample_analysis.process(user.getUserAsJson())
        type = predict(data)
        result[type].append(name)

    for k, v in result.iteritems():
        print "{}: {}".format(k, v)

if __name__ == '__main__':
    main("bmw")