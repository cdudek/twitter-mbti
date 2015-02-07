from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
import csv
path = "data"


def process(data):
    n=0
    for item in data['tweets'].values():
        # print len(data['tweets'][item]['entities']['user_mentions'])
        n=n + len(item["entities"]["user_mentions"])
    #print n , " " , len(data['tweets'])
    usr_mentions_per_tweet=round(n/float(len(data['tweets'])),4)
    return [usr_mentions_per_tweet]

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