import json
from models.User import User
from controller.UserController import UserController
import os
from os import listdir
from os.path import isfile, join
from Sample import Sample

import random

random.seed(32425)

class Dummy:
    def __init__(self):
        pass

    def predict(self, data):
        type = [0, 0, 0, 0]
        for i in range(4):
            if random.random() > 0.5:
                type[i] = 1
        return type

def loadML():
    return Dummy()

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

def main(eval_name, ml):
    uc = UserController()
    followers = uc.getFollowers(eval_name)
    directory = "followers_{}".format(eval_name)
    full_directory = "data/{}".format(directory)
    if not os.path.exists(full_directory):
        os.makedirs(full_directory)

    for name in followers:
        user = User(name, "{}/unknown".format(directory, name))
        if user.valid:
            user.writeFile()

    path = "data/followers_{}".format(eval_name)
    follower_files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    result = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    type = [i, j, k, l]
                    result[decodeType(type)] = []


    for file in follower_files:
        follower = Sample("{}/{}".format(path, file))
        type = ml.predict(follower.data)
        result[decodeType(type)].append(follower.twitName)

    with open("evaluated/follower_types_{}.json".format(eval_name), "w") as f:
        json.dump(result, f)

if __name__ == '__main__':
    main("bmw", loadML())