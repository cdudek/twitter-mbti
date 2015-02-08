__author__ = 'Zera'
import json
import os.path

def get_follower_types(name):
    filename = "evaluated/follower_types_{}.json".format(name)
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    else:
        return {}

print get_follower_types("bmw")