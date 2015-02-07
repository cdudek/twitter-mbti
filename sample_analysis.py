from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
import csv
path = "data"


def process(data):
    return [0]

files = [ f for f in listdir(path) if isfile(join(path,f)) ]

with open('samples.csv', 'w') as outfile:
    for file in files:
        type = file[0:4]
        twitName = file[5:-5]
        print "{}: {}".format(type, twitName)
        with open("data/{}".format(file)) as json_data:
            data = json.load(json_data)
            json_data.close()
            features = []
            features.append(twitName)
            features.append(type)
            features.extend(process(data))
            outwriter = csv.writer(outfile, lineterminator= '\n')
            outwriter.writerow(features)