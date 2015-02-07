from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
import csv
path = "data"


def process(data):
    n=[0,0,0,0,0];
    #n={'symbols':0,'user_mentions':0,'hashtags':0,'urls':0,'media':0};
    for tweet in data['tweets'].values():
        for entity in enumerate(tweet['entities']):
            n[entity[0]]=n[entity[0]]+len(tweet['entities'][entity[1]])
    #print n , " " , len(data['tweets'])
    usr_interactions_per_tweet = [round(x / float(len(data['tweets'])),4) for x in n]
    return [usr_interactions_per_tweet]

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